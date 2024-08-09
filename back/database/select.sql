# getUser
select *
from user
where user_id = '%s';

# findClub
select *
from club
where name like '%%s%';

# findFood
select *
from food
where place_name like '%%s%';


# getUserClubs
select *
from club
where club_id in (select club_id from user_club where user_id = '%s');

# getClubMembers
select user.*, label from user, user_club where user.user_id = user_club.user_id and club_id = 1;

# getClubEvents
select event.*, club.cover, club.name, user.real_name from event, club, user where event.club_id = 1001 and event.status = 2 and club.club_id = event.club_id and user.user_id = event.user_id;

# getClubNotices
select * from notice where club_id = '%s';

# getClubRequests(返回user列表, 并且要求请求未处理(status=0))
select * from user where user_id in (select applicant_id from joining_club where (club_id = '%s' and status = 0));

# quitClub(get master, name)
select master_id from club where club_id = '%s';
select name from club where club_id = '%s';

# getMessages
select * from message where receiver_id = '%s';

# getClubPosts
select post.*, user.avatar, user.real_name from post, user where club_id = 1001 and post.user_id = user.user_id;

# getPostReplies
select post.*, avatar, real_name from post, user where post_id = 1 and post.user_id = user.user_id;

# getOnePost
select * from post where post_id = 1;