CREATE TABLE api_requests(
	admin_id VARCHAR(25),
    call_date DATE,
    call_time TIME,
    result ENUM('success','failed'),
    error_counts INT
);