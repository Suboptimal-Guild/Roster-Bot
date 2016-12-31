from texttable import Texttable

from google.sheets import get_roster

async def print_roster(client, message):
    header, tanks, melee, ranged, healers = get_roster_strings()

    await client.send_message(message.channel, header)
    await client.send_message(message.channel, tanks)
    await client.send_message(message.channel, melee)
    await client.send_message(message.channel, ranged)
    await client.send_message(message.channel, healers)

async def add_to_roster(client, message):
    # format: !roster add <name> <role> <class> <spec> <rank>
    s = message.content.split()

async def remove_from_roster(client,message):
    # format: !roster remove <name>
    s = message.content.split()

    with open('roster.csv', 'r') as in_file, open('roster_edit.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        for row in csv.reader(in_file):
            if row[0] != s[2]:
                writer.writerow(row)

    # at this point, roster_edit.csv has our correct updated roster, so we need to transfer back to roster.csv
    with open('roster_edit.csv', 'r') as in_file, open('roster.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        for row in csv.reader(in_file):
            writer.writerow(row)

    await client.send_message(message.channel, ":banana: Removed **" + s[2] + "** from roster! :cry: :banana:")

    new_roster_string = get_roster_string()
    await client.send_message(message.channel, new_roster_string)

def get_roster_strings():
    roster = get_roster()

    header_string = ":banana: Roster for Suboptimal *(" + str(len(roster)) + " members total)* :banana:"

    table_dict = {}

    table_dict['T'] = [["Name", "Class", "Spec", "Rank"]]
    table_dict['M'] = [["Name", "Class", "Spec", "Rank"]]
    table_dict['R'] = [["Name", "Class", "Spec", "Rank"]]
    table_dict['H'] = [["Name", "Class", "Spec", "Rank"]]

    for player in roster:
        table_dict[player[1]].append([player[0], player[2], player[3], player[4]])

    # Helper function so we repeat ourselves less.
    def get_roster_print(header, rows):
        t = Texttable()
        t.add_rows(rows)
        return str(header + '\n```' + t.draw() + "```")

    tank_string = get_roster_print('**TANKS**', table_dict['T']) # Add tanks to our output.
    melee_string = get_roster_print('**MELEE**', table_dict['M']) # Add melee to our output.
    ranged_string = get_roster_print('**RANGED**', table_dict['R']) # Add ranged to our output.
    healer_string = get_roster_print('**HEALERS**', table_dict['H']) # Add healers to our output.

    return header_string, tank_string, melee_string, ranged_string, healer_string
