use food_system;

delimiter ;;



create trigger update_foodstatus
    BEFORE update on dish1
    for each row
begin
    if OLD.`like` = 0 and NEW.`like` = 1 then
        update food set `like` = `like` + 1, score = score + 1 where food_id = OLD.food_id;
    elseif OLD.`like` = 1 and NEW.`like` = 1 then
        update food set `like` = `like` - 1, score = score - 1 where food_id = OLD.food_id;
        set new.`like` = 0 ;
    elseif OLD.`like` = -1 and NEW.`like` = 1 then
        update food set `like` = `like` + 1, dislike = dislike - 1, score = score + 2 where food_id = OLD.food_id;  
    elseif OLD.`like` = 0 and NEW.`like` = -1 then
        update food set dislike = dislike + 1, score = score - 1 where food_id = OLD.food_id;      
    elseif OLD.`like` = 1 and NEW.`like` = -1 then
        update food set dislike = dislike + 1, `like` = `like` - 1, score = score - 2 where food_id = OLD.food_id; 
    elseif OLD.`like` = -1 and NEW.`like` = -1 then
        update food set dislike = dislike - 1, score = score + 1 where food_id = OLD.food_id; 
        set new.`like` = 0;
    end if ;    
end ;;


delimiter ;
