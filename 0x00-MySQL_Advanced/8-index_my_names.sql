-- creates an index on the first letter of name a column in a table
CREATE INDEX idx_name_first ON names (name(1));
