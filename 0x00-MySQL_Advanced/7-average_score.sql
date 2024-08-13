-- a stored procedure that computes and stores average score for a student
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser (IN in_user_id INT)
BEGIN
	DECLARE avg_score FLOAT;
	DECLARE total_score FLOAT;
	DECLARE total_rows INT;
	-- calculate scores associate with the user id then divide with the number of the scores
	SELECT SUM(score), COUNT(score) INTO total_score, total_rows
 	FROM corrections WHERE user_id = in_user_id;

	SET avg_score = total_score / total_rows;

	-- store avg score in a table
	UPDATE users
	SET average_score = avg_score
	WHERE id = in_user_id;
END//

DELIMITER ;
