from flask import Flask, request, jsonify
import sqlite3
conn = sqlite3.connect("football_stats.db")
cursor = conn.cursor()

# Lister toutes les tables présentes
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

conn.close()

print("📋 Tables existantes dans la base de données :", tables)