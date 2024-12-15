# Task Manager
A web application that allows users to manage tasks efficiently. The application provides features like creating, updating, and deleting tasks, assigning executors, categorizing tasks with labels, and managing their statuses.

[Live Website](https://task-manager-eqwt.onrender.com/)

### Hexlet tests and linter status:
[![Actions Status](https://github.com/anna-at-sea/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/anna-at-sea/python-project-52/actions)
[![Python CI](https://github.com/anna-at-sea/python-project-52/actions/workflows/CI.yml/badge.svg)](https://github.com/anna-at-sea/python-project-52/actions/workflows/CI.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/bc834ccad90ad84f532d/maintainability)](https://codeclimate.com/github/anna-at-sea/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/bc834ccad90ad84f532d/test_coverage)](https://codeclimate.com/github/anna-at-sea/python-project-52/test_coverage)

### System requirements:
* python = "^3.10"
* poetry = "^1.4.2"

### Installation:
1. Clone the repository
1. Rename .env.sample:
    `mv .env.sample .env`
2. Set up environmantal variables in .env file
3. Install dependencies:
    `make install`
4. Apply database migrations:
    `make migrate`

### Run server locally:
`make dev`