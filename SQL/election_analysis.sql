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
	max(case when vote_rank = 2 then candidate end) as runnerup_candidate,
	max(case when vote_rank=2 then party end) as runnerup_party
from candidate_rank
group by constituency, province, district;
	
select count(*) from winner_and_runnerup
where winner_party = 'RSP';

