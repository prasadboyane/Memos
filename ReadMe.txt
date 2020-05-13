# Memos
Memos is Desktop app to made in pyhton to manage your memos. You need to login as an user then you can see your all memos.
Only Admin user has access to add new uesrs.
You can perform below operations:
1. Create Memo
2. Delete Memo
3. Edit Memo

Dependancies:
pip install tkinter
pip install mysql-connector-python

# App flow:
1. You need to login as Admin user and create a new user. The user info will store in Mysql databse in 'users' table
2. Exit the app and login again as normal user and start creating memos. This memos will be stored/fetched from 'user_memos' table

# Database pre-requisites:

Create Schema:
create database 'memos'

Create tables:

CREATE TABLE `user_memo` (
  `username` varchar(30) DEFAULT NULL,
  `title` varchar(30) DEFAULT NULL,
  `body` varchar(30) DEFAULT NULL,
  `create_dtm` timestamp NULL DEFAULT NULL,
  `update_dtm` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `users` (
  `username` varchar(30) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
