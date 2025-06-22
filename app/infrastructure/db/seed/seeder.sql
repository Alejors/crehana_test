INSERT IGNORE INTO users (id, username, email, password)
VALUES 
  (1, 'user1', 'user1@example.com', '$2b$12$F1DlWKoiKLMMnjT/n0Q56eedZK/lmUvxGk3EO5QYI55VXYuNYTZ2y'),
  (2, 'user2', 'user2@example.com', '$2b$12$F1DlWKoiKLMMnjT/n0Q56eedZK/lmUvxGk3EO5QYI55VXYuNYTZ2y'),
  (3, 'user3', 'user3@example.com', '$2b$12$F1DlWKoiKLMMnjT/n0Q56eedZK/lmUvxGk3EO5QYI55VXYuNYTZ2y'),
  (4, 'user4', 'user4@example.com', '$2b$12$F1DlWKoiKLMMnjT/n0Q56eedZK/lmUvxGk3EO5QYI55VXYuNYTZ2y');

INSERT IGNORE INTO task_lists (id, name)
VALUES 
  (1, 'list1'),
  (2, 'list2'),
  (3, 'list3');

INSERT IGNORE INTO tasks (id, description, task_list_id, is_completed, priority, assigned_user_id)
VALUES
  (1, 'Tarea 1 de list1', 1, false, 'low', NULL),
  (2, 'Tarea 2 de list1', 1, true,  'medium', NULL),
  (3, 'Tarea 3 de list1', 1, false, 'high', NULL),

  (4, 'Tarea 1 de list2', 2, true,  'medium', NULL),
  (5, 'Tarea 2 de list2', 2, false, 'low', NULL),

  (6, 'Tarea 1 de list3', 3, true,  'medium', 1),
  (7, 'Tarea 2 de list3', 3, true,  'high', 2),
  (8, 'Tarea 3 de list3', 3, false, 'medium', 3);
