
Season ticket planner
=====================

Just a simple Python script that advises what season ticket to buy, given the
ticket prices/validities and the travel forecast.

All parameters are taken from environment variables instead of command line
arguments.

All dates are in `YYYYMMDD` format.

The below are the environment variables:

| Variable | Optional/Mandatory | Description |
| -------- | ------------------ | ----------- |
| `tickets` | Mandatory | File describing ticket types. See below format. |
| `plan` | Mandatory | File containing journey plan. See below format. |
| `has_days`,`has_left` | Optional | When you already hold a valid ticket, specify how many travel days are in credit, and for how many days the ticket is valid. Defaults are 0. |

Typical invocation would look like:

```bash
plan=plan tickets=tickets has_days=2 has_left=5 ./planner.py
```

Which translates to: The journey plan is in the file `plan`; ticket types are in
the file `ticket`; and I already have a ticket with which I can travel for 2
days in the next 5 days.

And example content for `tickets` file is below:

```
# name,  no. of days you can travel, no. days it's valid for, and price
daily   1   1   50.3
weekly  7   7   140.2
flexi   8   28  352.1
monthly 30  30  538.4
```

And a `plan` file:

```
# Either a single date.
# or a date plus no. continuous days (default: 1) starting from the given date (inclusive)
# Only dates >= today are counted
# With the below, the travel dates are: ['20210920', '20210923', '20210927', '20210928']
20210920
20210923 1
20210927 2
```

<!-- vim: set tw=80: -->
