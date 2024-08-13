-- a stored procedure that adds a new correction for a student
DELIMITER //

CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
	DECLARE project_id INT;

	-- Retrieve the project_id based on project name
        SELECT id INTO project_id
	FROM projects
	WHERE projects.name = project_name;

	-- if project doesnt exist, add a new project
        IF project_id IS NULL THEN
		INSERT INTO projects (name) VALUES (project_name);
		SET project_id = LAST_INSERT_ID();
	END IF;

	INSERT INTO corrections (user_id, project_id, score) VALUES (user_id, project_id, score);
END//

DELIMITER ;
