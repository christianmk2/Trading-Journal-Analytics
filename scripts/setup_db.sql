-- setup_db.sql — run once with: psql -U postgres -f setup_db.sql
CREATE USER trader WITH PASSWORD 'admin';
CREATE DATABASE trading_journal OWNER trader;