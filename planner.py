#!/usr/bin/env python3

from copy import deepcopy
from datetime import date, datetime, timedelta
import os


class TicketType:
    def __init__(self, name, days, valid_for, cost):
        self.name = name
        self.days = days
        self.valid_for = valid_for
        self.cost = cost

    @staticmethod
    def from_line(line):
        name, days, valid_for, cost = line.split()
        return TicketType(name, int(days), int(valid_for), float(cost))

    def __repr__(self):
        return f"TicketType name={self.name} {self.days}/{self.valid_for}"


class Wallet:
    def __init__(self, days_credit=0, days_left=0):
        self.days_credit = days_credit
        self.days_left = days_left
        self.cost = 0
        self.log = []

    def buy_ticket(self, day, ticket):
        self.days_credit += ticket.days
        self.days_left += ticket.valid_for
        self.cost = round(self.cost + ticket.cost, 2)
        self.log += [f"{day}: buy {ticket.name} total_cost={self.cost}"]

    def has_credit(self):
        return self.days_left > 0 and self.days_left > 0

    def travel(self):
        self.days_credit -= 1
        self.expire()

    def expire(self):
        if self.days_left > 0:
            self.days_left -= 1

    def __repr__(self):
        return f"Wallet credit={self.days_credit} left={self.days_left}"


def read_travel_days(file_name):
    ret = set()
    with open(file_name) as fd:
        for line in fd:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            fields = line.split()

            if len(fields) not in {0, 1, 2}:
                raise Exception(f"Invalid entries: {fields}")

            if len(fields) == 1:
                # For assertion only
                datetime.strptime(fields[0], FORMAT)
                ret.add(fields[0])
            elif len(fields) == 2:
                start = datetime.strptime(fields[0], FORMAT)
                num = int(fields[1])

                if num <= 0:
                    raise Exception(f"Invalid entries: {fields}")

                for i in range(num):
                    ret.add((start + timedelta(days=i)).strftime(FORMAT))

    return ret


def read_ticket_types(file_name):
    ret = []
    with open(file_name) as fd:
        for line in fd:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            ret.append(TicketType.from_line(line))

    return ret


FORMAT = "%Y%m%d"
NEXT_DAY = timedelta(days=1)


def plan(wallet, current_day, travelling_days, ticket_types, all_wallets):
    while True:
        if not travelling_days:
            break

        today = current_day.strftime(FORMAT)
        if today in travelling_days:
            if not wallet.has_credit():
                break

            wallet.travel()
            travelling_days.remove(today)
        else:
            wallet.expire()

        current_day += NEXT_DAY

    if not travelling_days:
        all_wallets.append(wallet)
        return

    for ticket in ticket_types:
        new_wallet = deepcopy(wallet)
        new_wallet.buy_ticket(current_day.strftime(FORMAT), ticket)

        plan(
            new_wallet,
            deepcopy(current_day),
            deepcopy(travelling_days),
            ticket_types,
            all_wallets)


def main():
    has_days = int(os.environ.get("has_days", "0"))
    has_left = int(os.environ.get("has_left", "0"))
    if has_days < 0:
        raise Exception(f"Invalid has_days: {has_days}")
    if has_left < has_days:
        raise Exception(f"Invalid has_left: {has_left}")

    travelling_days = read_travel_days(os.environ["plan"])
    start_str = date.today().strftime(FORMAT)
    valid_days = {d for d in travelling_days if d >= start_str}
    if len(valid_days) == 0:
        raise Exception("No valid travel days")

    ticket_types = read_ticket_types(os.environ["tickets"])
    if len(ticket_types) == 0:
        raise Exception("No valid ticket types")

    all_wallets = []
    plan(
        Wallet(has_days, has_left),
        datetime.strptime(start_str, FORMAT),
        valid_days,
        ticket_types,
        all_wallets)

    min_wallets = [all_wallets[0]]
    for w in all_wallets[1:]:
        if w.cost == min_wallets[0].cost:
            min_wallets.append(w)
        elif w.cost < min_wallets[0].cost:
            min_wallets = [w]

    print(f"Ticket purchases for {sorted(valid_days):}")
    print(f"Found {len(min_wallets)} solutions:")
    print("\n OR\n".join(["\n".join(w.log) for w in min_wallets]))


if __name__ == "__main__":
    main()


# vim: set tw=80:
