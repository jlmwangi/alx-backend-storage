-- lista all students with score under 80 and no last_meeting or more than one month
DROP VIEW IF EXISTS need_meeting;

CREATE VIEW need_meeting AS
SELECT name FROM students
WHERE score < 80 AND (last_meeting IS NULL OR last_meeting < CURDATE() - INTERVAL 1 MONTH);
