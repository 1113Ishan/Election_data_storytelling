create table elections(
	province text, 
	candidate text, 
	votes int, 
	winner boolean, 
	district_name text, 
	constituency text, 
	party text, 
	election_year smallint
);


alter table elections 
rename column district_name to district; 

select * from elections;

create view candidate_rank as
select
	province, 
	district, 
	constituency,
	candidate, 
	party,
	votes,
	winner,
	rank () over(partition by province, district, constituency order by votes desc) as vote_rank
from elections;

select * from candidate_rank;


create view winner_and_runnerup as
select 
	constituency,
	province, 
	district,
	max(case when vote_rank = 1 then candidate end) as winner_candidiate,
	max(case when vote_rank = 1 then party end) as winner_party,
	max(case when vote_rank = 1 then votes end) as winner_votes,
	max(case when vote_rank = 2 then candidate end) as runnerup_candidate,
	max(case when vote_rank=2 then party end) as runnerup_party,
	max(case when vote_rank = 2 then votes end) as runner_up_votes
from candidate_rank
group by constituency, province, district;

select * from winner_and_runnerup;
	
create view win_margin_analysis as
select 
	province, 
	district,
	constituency,
	winner_party,
	winner_votes,
	runnerup_party,
	runner_up_votes,
	(winner_votes - runner_up_votes) as vote_difference,
	(((winner_votes::decimal) - (runner_up_votes::decimal)) / (winner_votes + runner_up_votes) * 100) as win_margin
from winner_and_runnerup;	


select * from win_margin_analysis;

alter view win_margin_analysis
rename column win_margin to win_percentage;


create view win_classification as
select 
	*, 
	case 
		when win_percentage < 5 then 'Close win'
		when win_percentage >= 5 and win_percentage < 25 then 'Competitive'
		else 'Safe win'
	end as win_status
	from win_margin_analysis;



create view win_status_count as
select 
	winner_party as party,
	count(case when win_status = 'Close win' then 1 end) as Close_wins,
	count(case when win_status = 'Competitive' then 1 end) as Competitive_wins,
	count(case when win_status = 'Safe win' then 1 end) as Safe_wins
from win_classification
group by winner_party;



create view win_distribution_province as
select
	a.province, 
	a.party,
	b.total_available_seats,
	a.total_wins
from(
	select
	province,
	party,
	count(*) as total_wins
from candidate_rank
where vote_rank = 1
group by province, party
) a
join(
	select 
	province, 
	count(*) as total_available_seats
from (
	select distinct province, district, constituency
	from elections
) seats
group by province
) b
on a.province = b.province
order by province;



CREATE TABLE fact_winners AS
SELECT
    province,
    district,
    constituency,
    candidate AS winner_candidate,
    party AS winner_party,
    votes AS winner_votes
FROM candidate_rank
WHERE vote_rank = 1;


CREATE TABLE fact_runnerups AS
SELECT
    province,
    district,
    constituency,
    candidate AS runnerup_candidate,
    party AS runnerup_party,
    votes AS runnerup_votes
FROM candidate_rank
WHERE vote_rank = 2;


CREATE TABLE fact_constituency_results AS
SELECT
    w.province,
    w.district,
    w.constituency,
    w.winner_candidate,
    w.winner_party,
    w.winner_votes,
    r.runnerup_candidate,
    r.runnerup_party,
    r.runnerup_votes,
    (w.winner_votes - r.runnerup_votes) AS vote_difference,
    ((w.winner_votes::decimal - r.runnerup_votes::decimal)
     / NULLIF((w.winner_votes + r.runnerup_votes), 0)) * 100 AS win_percentage
FROM fact_winners w
JOIN fact_runnerups r
ON w.province = r.province
AND w.district = r.district
AND w.constituency = r.constituency;



CREATE TABLE fact_province_summary AS
SELECT
    province,
    winner_party AS party,
    COUNT(*) AS seats_won
FROM fact_winners
GROUP BY province, winner_party;

