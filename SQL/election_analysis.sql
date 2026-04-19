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

alter view win_margin_analysis
rename column win_margin to win_percentage;

select count(*) from win_margin_analysis;

select count(*) from win_margin_analysis
where win_percentage < 20;



create view win_classification as
select 
	*, 
	case 
		when win_percentage < 5 then 'Close win'
		when win_percentage >= 5 and win_percentage < 25 then 'Competitive'
		else 'Safe win'
	end as win_status
	from win_margin_analysis;

select * from win_classification;

select 
	winner_party as party,
	win_status,
	count(*) as seats
from win_classification
group by winner_party, win_status;

create view win_status_count as
select 
	winner_party as party,
	count(case when win_status = 'Close win' then 1 end) as Close_wins,
	count(case when win_status = 'Competitive' then 1 end) as Competitive_wins,
	count(case when win_status = 'Safe win' then 1 end) as Safe_wins
from win_classification
group by winner_party;

select * from win_status_count;
	
	
	
	