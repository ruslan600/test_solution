select date, rec_result, project_id, server_id, count(rec_result) as total_count,
sum(duration) as total_duration
from recognition_results
inner join project on recognition_results.project_id = project.id
inner join server on recognition_results.server_id = server.id
where date between 'date1' and 'date2'
group by date, rec_result, project_id, server_id;