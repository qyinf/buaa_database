use club_system;

select allocId();

-- insert into user(`user_id`, `password`, `time`, `email`, `followers`, `following`)
-- values ('u_c', 'c', from_unixtime(unix_timestamp()), 'sb', 0, 0),
--        ('u_b', 'b', from_unixtime(unix_timestamp()), 'sb', 0, 0),
--        ('20373742', '12345678a', from_unixtime(unix_timestamp()), 'sb', 0, 0);
-- # select * from user;
--
-- insert into club(club_id, name, member_count, type, master_id, time, intro, status) value (1001, '机器人社', 0, 2, 'u_b', from_unixtime(unix_timestamp()), '%s', 0);
-- insert into club(club_id, name, member_count, type, master_id, time, intro, status) value (1002, '凌峰社', 0, 2, 'u_c', from_unixtime(unix_timestamp()), '%s', 0);
-- # select * from club;
--
-- insert into event(event_id, club_id, user_id, content, time, apply_time, expired_time, begin_time, end_time, member_count, member_limit, status) values (2001, 1001, '20373742', 'event1', from_unixtime(unix_timestamp()), from_unixtime(unix_timestamp()), from_unixtime(unix_timestamp()), from_unixtime(unix_timestamp()), from_unixtime(unix_timestamp()), 1, 200, 2);
-- insert into event(event_id, club_id, user_id, content, time, apply_time, expired_time, begin_time, end_time, member_count, member_limit, status) values (2002, 1001, '20373742', 'event2', from_unixtime(unix_timestamp()), from_unixtime(unix_timestamp()), from_unixtime(unix_timestamp()), from_unixtime(unix_timestamp()), from_unixtime(unix_timestamp()), 1, 300, 2);
--
-- insert into joining_club values (3, '20373742', 1001, 0, from_unixtime(unix_timestamp()));
-- # call handleJoiningClub(0, 3);
--
-- select * from user, joining_club where user_id in (select applicant_id from joining_club where (club_id = 1001 and status = 0))