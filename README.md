<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Copy README</title>
<style>
  body { font-family: monospace; white-space: pre-wrap; margin: 20px; }
  button {
    background-color: #5865F2;
    color: white;
    border: none;
    padding: 10px 15px;
    cursor: pointer;
    border-radius: 5px;
    font-size: 16px;
    margin-bottom: 15px;
  }
  button:hover {
    background-color: #4752c4;
  }
  #content {
    border: 1px solid #ddd;
    padding: 15px;
    max-height: 500px;
    overflow-y: scroll;
    background-color: #f9f9f9;
  }
</style>
</head>
<body>

<button onclick="copyText()">📋 Copy README</button>

<div id="content">
# Crunchyroll Account Checker

A Python script to check Crunchyroll account validity with proxy support and sending valid/custom accounts to a Discord webhook.

---

## Requirements

- Python 3.8 or higher installed  
- Google Chrome installed (used by Selenium)  
- Internet connection  
- Discord webhook URL (to receive valid/custom accounts)

---

## Installing dependencies

Open your terminal and run:

```bash
pip install selenium webdriver-manager requests

1. Setup
Clone or download this repository
git clone https://github.com/your-username/your-repo.git
cd your-repo

Run the script

```python checker.py```
