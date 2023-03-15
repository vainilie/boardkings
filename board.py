from rich import print
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.prompt import Confirm, Prompt, IntPrompt
from art import text2art
import json
from rich.theme import Theme

theme = Theme.read("styles")
console = Console(theme=theme)
f = open("board.json", "r")
data = json.load(f)
albums = data
album = albums["albums"][0]
accs = album["accounts"]


# % ─── FUNCTIONS ──────────────────────────────────────────────────────────── ✰ ─
# & ──────────────── Progress Bar ──────────────── #
def progressbar(value, maxval, leng):
    """Creates a progress bar"""
    val = (leng / maxval) * value
    bar = ""
    while val > 0:
        if val < 1 and val >= 0.5:
            bar = bar + "▒"
        elif val < 1 and val < 0.5:
            break
        else:
            bar = bar + "█"
        val -= 1
    while len(bar) < leng:
        bar += "░"
    return bar


# & ────────────────── Save File ───────────────── #
def save():
    """save file"""
    with open("board.json", "w") as outfile:
        json.dump(albums, outfile, indent=4)


# & ────────────── String generator ────────────── #
def get_str(account, emojis):
    """generate the string for display by cell"""
    display = []
    for idx, a_set in enumerate(album["sets"]):
        strings = []
        for idc, card in enumerate(a_set["cards"]):
            if card[2] is True:
                if account["sets"][idx][idc] > 1:
                    string = emojis[0]
                elif account["sets"][idx][idc] == 1:
                    string = emojis[1]
                else:
                    string = emojis[2]
            else:
                if account["sets"][idx][idc] > 0:
                    string = emojis[3]
                else:
                    string = emojis[4]
            strings.append(string)
        display.append(strings)
    return display


# & ─────────────── Update account ─────────────── #
def update_account(acc):
    """update all account"""
    extra = 0
    missing = []
    spares = []
    total = 0
    mis = 0
    sets = acc["sets"]
    tTotal = 0
    tMiss = 0
    tradeable = 0
    for idx, a_set in enumerate(album["sets"]):
        miss = []
        spare = []
        for idc, card in enumerate(a_set["cards"]):
            if card[2] is True:
                tradeable += 1
                if sets[idx][idc] > 1:
                    extra += (sets[idx][idc] * card[1]) - card[1]
                    total += 1
                    spare.append(card[0])
                    tTotal +=1
                elif sets[idx][idc] == 1:
                    total += 1
                    tTotal += 1
                else:
                    miss.append(card[0])
                    mis += 1
                    tMiss += 1
            else:
                if sets[idx][idc] > 0:
                    extra += (sets[idx][idc] * card[1]) - card[1]
                    total += 1
                else:
                    mis += 1
        missing.append(miss)
        spares.append(spare)
    acc.update(
        {
            "total": total,
            "missing": missing,
            "spares": spares,
            "extra": extra,
            "percentage": str(round((total * 100) / album["stats"]["total"], 1)) + "%",
            "tradeable": "+" + str(tTotal) + " | -" + str(tMiss),
            "percentage trades": str(round((tTotal * 100) / (album["stats"]["tradeable"] ), 1)) + "%",
            "trades bar": progressbar(tTotal, (album["stats"]["tradeable"]), 15),
            "progress": "+" + str(total) + " | -" + str(mis),
            "bar": progressbar(total, album["stats"]["total"], 15),
        }
    )
    save()


# & ───────────────── Update JSON ──────────────── #
def update_all():
    """update the data in json"""
    str_emojis = [
        [
            ":carrot:",
            ":small_orange_diamond:",
            ":small_red_triangle_down:",
            ":sunflower:",
            ":white_medium_square:",
        ],
        [
            ":rabbit2:",
            ":small_blue_diamond:",
            ":small_red_triangle:",
            ":hibiscus:",
            ":white_medium_square:",
        ],
    ]
    for idx, acc in enumerate(accs):
        display = get_str(acc, str_emojis[idx])
        update_account(acc)
        acc.update({"display": display})
    save()


# & ────────────────── list2set ────────────────── #
def l2s(list1):
    """turn list to set"""
    s = set()
    for x in list1:
        s.add(x)
    return s


# & ───────────────── update set ───────────────── #
def update_set(a, s, c):
    acc = accs[a]["sets"]
    acc[s] = c
    update_account(accs[a])


# & ───────────── update single card ───────────── #
def update_single(a, s, c, n):
    acc = accs[a]["sets"]
    sset = acc[s]
    sset[c] = n
    update_account(accs[a])


# !% ────────────────────────────────────────────────────────── END FUNCTIONS ─────
# % ─── DISPLAY FUNCTIONS ──────────────────────────────────────────────────── ✰ ─
# & ───────────────── Print Stars ──────────────── #
def get_stars():
    """get stars"""
    stars.add_column(justify="right")
    stars.add_column(no_wrap=True)
    stars.add_column(justify="right")

    for idx, star in enumerate(album["stats"]["stars"]):
        stars.add_row(":star:" * (idx + 1), " ", str(star))
    stars.add_row("")
    stars.add_row("[color9][b]sets", " ", str(album["stats"]["sets"]))
    stars.add_row("[color7][b]tradeable", " ", str(album["stats"]["tradeable"]))
    stars.add_row(
        "[color11][b]untradeable", " ", str(album["stats"]["untradeable"]))
    stars.add_row("[color10][b]total", " ", str(album["stats"]["total"]))


# & ───────────────── Print Stats ──────────────── #
def get_stats():
    """get stats by account"""
    stats.add_column("[color0]Account", style="color0 b", justify="right")
    stats.add_column(
        f"[color11]{accs[0]['name']}",
        no_wrap=True,
        justify="right",
    )
    stats.add_column(f"[color5]{accs[1]['name']}", no_wrap=True, justify="right")
    for key in accs[0]:
        if type(accs[0][key]) is list:
            pass
        elif key == "name":
            pass
        else:
            stats.add_row(key, str(accs[0][key]), str(accs[1][key]))


# & ─────────────── Print emoji table ────────────── #
def get_emojis():
    """to get the emoji table content"""
    emoji_table.add_column(
        "[color0 b]set",
        style="color0",
        no_wrap=True,
        justify="right",
    )
    idx = 0
    while idx < 12:
        emoji_table.add_column(
            f"[color{idx}]{str(idx + 1).zfill(2)}",
            style=f"color{idx}",
            no_wrap=True,
            justify="center",
        )
        idx += 1
    emoji_table.add_column(
        "[color0 b]total",
        style="color0 b",
        no_wrap=True,
        justify="right",
    )
    for idx, a_set in enumerate(album["sets"]):
        string = []
        title = f"{str(idx + 1).zfill(2)}. {a_set['title']}"
        for idy, a_card in enumerate(a_set["cards"]):
            if (
                accs[0]["display"][idx][idy] or accs[1]["display"][idx][idy]
            ) == ":white_medium_square:":
                space = " "
            else:
                space = ""
            cell = accs[0]["display"][idx][idy] + space + (accs[1]["display"][idx][idy])
            string.append(cell)
        total0 =  12 - accs[0]["sets"][idx].count(0)
        total1 = 12 - accs[1]["sets"][idx].count(0)
        if total0 == 12:
            total0 = ":heavy_check_mark:"
        else:
            total0 = str(total0)
        if total1 == 12:
            total1 = ":heavy_check_mark:"
        else:
            total1 = str(total1)

        emoji_table.add_row(
            title,
            string[0],
            string[1],
            string[2],
            string[3],
            string[4],
            string[5],
            string[6],
            string[7],
            string[8],
            string[9],
            string[10],
            string[11],
            total0 + " " + total1,
            style=f"color{idx + 1}",
        )


# & ──────────────── Print trades ──────────────── #
def get_trades(acc1, acc2):
    idx = 0
    trades.add_column(
        "[color9 b]set",
        style="color9",
        no_wrap=True,
        justify="right",
    )
    trades.add_column(
        f"[color{idx + 2}]{acc1['name']} :arrow_right: {acc2['name'][:2]}",
        style=f"color{idx}",
        no_wrap=True,
        justify="left",
    )
    trades.add_column(
        f"[color{idx + 4}]{acc2['name'][:2]} :arrow_right: {acc1['name']}",
        style=f"color{idx}",
        no_wrap=True,
        justify="left",
    )
    while idx < 12:
        trade1 = l2s(acc1["spares"][idx]).intersection(l2s(acc2["missing"][idx]))
        trade2 = l2s(acc2["spares"][idx]).intersection(l2s(acc1["missing"][idx]))
        tr1 = []
        tr2 = []
        for x in trade1:
            tr1.append(x.__str__())
        for x in trade2:
            tr2.append(x.__str__())
        if (len(tr1) or len(tr2)) > 0:
            t1 = ", ".join(tr1)
            t2 = ", ".join(tr2)
            trades.add_row(f"[color{idx + 1}][b]Set {idx + 1}[/]", t1, t2)
        idx += 1


# & ──────────────── Print number ──────────────── #
def get_numbers():
    """to get tiny data by number"""
    idx = 0
    idy = 0
    while idx < 25:
        if idx == 12:
            numbers.add_column(
                "[color0 b]S E T", style="bold", no_wrap=True, justify="center"
            )
            idy = 0
        else:
            numbers.add_column(
                f"[color{idy}]{str(idy + 1)}",
                style=f"color{idy}",
                no_wrap=True,
                justify="right",
            )
            idy += 1
        idx += 1
    for idx, a_set in enumerate(album["sets"]):
        str1 = []
        str2 = []
        title = f"{str(idx + 1).zfill(2)}. {a_set['title']}"
        for idy, a_card in enumerate(a_set["cards"]):
            str1.append(str(accs[0]["sets"][idx][idy]))
            str2.append(str(accs[1]["sets"][idx][idy]))
        numbers.add_row(
            str1[0],
            str1[1],
            str1[2],
            str1[3],
            str1[4],
            str1[5],
            str1[6],
            str1[7],
            str1[8],
            str1[9],
            str1[10],
            str1[11],
            title,
            str2[0],
            str2[1],
            str2[2],
            str2[3],
            str2[4],
            str2[5],
            str2[6],
            str2[7],
            str2[8],
            str2[9],
            str2[10],
            str2[11],
            style=f"color{idx + 1}",
        )


# !% ────────────────────────────────────────────────── END DISPLAY FUNCTIONS ─────
# % ─── PROMPT FUNCTIONS ───────────────────────────────────────────────────── ✰ ─
# & ──────────── select single update ──────────── #
def ask_card(acc, sett):
    while True:
        card = IntPrompt.ask(
            """Please select the card number, between [b]1[/b] and [b]12[/b].
            [b]0[/] for quit. [b]13[/] to return"""
        )
        if card == 0:
            exit()
        elif card == 13:
            ask_update(acc, sett)
        elif card <= 12:
            carrd = card - 1
            break
        print("[b] :pile_of_poo: [prompt.invalid]Number must be between 1 and 12")
    print(f"[b] [:carrot:] Set number {sett + 1}: card {card}")
    ask_new(acc, sett, carrd)


# & ────────────── select new spare ────────────── #
def ask_new(acc, sett, carrd):
    while True:
        spare = IntPrompt.ask(
            f"""Please put how many spares of {carrd + 1} do you have.
            Currently: {str(accs[acc]["sets"][sett][carrd])}
            [b]666[/] for quit. [b]66[/] to return"""
        )
        if spare == 666:
            exit()
        elif spare == 66:
            ask_card(acc, sett)
        else:
            break
        print("[b] :pile_of_poo: [prompt.invalid]Number must be an integrer")
    print(
        f"[b]UPDATING: [:carrot:] Set number {sett + 1}: card {carrd+1}: spares {spare}"
    )
    update_single(acc, sett, carrd, spare)
    if Confirm.ask(
        f"Continue updating in the {accs[acc]['name']} account, set {sett+1}?",
        default=False,
    ):
        ask_card(acc, sett)
    else:
        ask_set(acc)


# & ────────────── select all update ───────────── #
def ask_string(acc, sett):
    c = [str(x) for x in accs[acc]["sets"][sett]]
    current = " ".join(c)
    while True:
        numbers = Prompt.ask(
            f"""Please enter how many cards do you have. Q for exit.
            C: [color3]1 2 3 4 5 6 7 8 9 0 1 2
            H: [color0]{current}
            N"""
        )
        if numbers == ("Q" or "q"):
            exit()
        else:
            cards = numbers.split(" ")
            print(cards)
            if len(cards) == 12:
                break
            print("[b] :pile_of_poo: [prompt.invalid]You must enter 12 numbers.")
    newcards = [int(x) for x in cards]
    update_set(acc, sett, newcards)
    if Confirm.ask(
        f"Continue updating in the {accs[acc]['name']} account?", default=False
    ):
        ask_set(acc)
    else:
        ask_account()


# & ─────────── select if all or single ────────── #
def ask_update(acc, sett):
    method = Prompt.ask(
        "[color0]Update all the set (s) or just a card (c)? (r) to return",
        choices=["s", "c", "r", "q"],
    )
    if method == "s":
        ask_string(acc, sett)
    elif method == "c":
        ask_card(acc, sett)
    elif method == "q":
        exit()
    elif method == "r":
        ask_set(acc)


# & ───────────────── select set ───────────────── #
def ask_set(acc):
    while True:
        Set = IntPrompt.ask(
            """Please select the set number, between [b]1[/b] and [b]12[/b].
            [b]0[/] to return. [b]13[/b] to quit."""
        )
        if Set == 0:
            ask_account()
        elif Set == 13:
            print("Byee! :wave:")
            exit()
        elif Set <= 12:
            sett = Set - 1
            break
        print("[b] :pile_of_poo: [prompt.invalid]Number must be between 1 and 12")
    c = [str(x).zfill(2) for x in accs[acc]["sets"][sett]]
    currentab = Table.grid(padding=1, expand=True)
    idx = 0
    while idx < 12:
        currentab.add_row(
            f"[b][color{idx + 1}]{c[idx]}[/]",
            f"[b][color{idx + 2}]{c[idx + 1 ]}[/]",
            f"[b][color{idx + 3}]{c[idx + 2]}[/]",
            f"[b][color{idx + 5}]{c[idx + 3]}[/]",
        )
        idx += 4
        mini = Panel.fit(
            currentab,
            box=box.ROUNDED,
            padding=(2, 1),
            title=f"[color6 b]:carrot:Set{Set}: [i]{album['sets'][sett]['title']}[/i]",
            subtitle=f"[color6 b][i]{accs[acc]['name']}[/i] :rabbit:",
            border_style="color6",
        )
    console.print(mini, justify="center")
    ask_update(acc, sett)


# & ─────────────── select account ─────────────── #
def ask_account():
    """ask what account"""
    account = Prompt.ask(
        "Select an account. [b]Y[/]u or [b]H[/]elena. [b]Q[/]uit",
        choices=["y", "h", "q"],
    )
    if account == "q":
        print("Byee :wave:")
        exit()
    elif account == "y":
        acc = 0
    else:
        acc = 1
    print(f"[b]:carrot: {accs[acc]['name']} account selected.")
    ask_set(acc)


def reset_all():
    empty_set = [0,0,0,0,0,0,0,0,0,0,0,0]
    set__ = 0
    while set__ < 12:
        update_set(0, set__, empty_set)
        update_set(1, set__, empty_set)
        set__ += 1
    update_all()
        

# !% ─────────────────────────────────────────────────── END PROMPT FUNCTIONS ─────
# % ─── DISPLAY ────────────────────────────────────────────────────────────── ✰ ─
# & ──────────────────── About ─────────────────── #
About = Text(text2art(album["title"], font="bolger"), justify="full", style="color11")
# & ──────────────────── Stars ─────────────────── #
stars = Table.grid()
get_stars()
Stars = Panel.fit(
    stars,
    box=box.ROUNDED,
    padding=(0, 1),
    border_style="color3",
)
# & ──────────────────── Stats ─────────────────── #
stats = Table(box=box.SIMPLE_HEAVY, style="color0", padding=(0, 1), pad_edge=False)
get_stats()
Stats = Panel.fit(
    stats,
    box=box.ROUNDED,
    padding=(0, 1),
    border_style="color0",
)
# & ───────────────── table cards ──────────────── #
emoji_table = Table(
    show_edge=True,
    show_header=True,
    expand=True,
    box=box.SIMPLE_HEAVY,
    border_style="color6",
    padding=(0, 0),
)
get_emojis()
# & ──────────────── table number ──────────────── #
row_styles = ["on #2d3437",""]
numbers = Table(
    show_edge=True,
    show_header=True,
    expand=False,
    box=box.SIMPLE_HEAD,
    show_lines=False,
    header_style="b",
    border_style="color6",
    row_styles=row_styles)
headers = Table.grid(expand=True)
headers.add_column(justify="center")
headers.add_column(justify="center")
headers.add_row(
    f"[color0 b]{accs[0]['name']}",
    f"[color6 b]{accs[1]['name']}",
)
get_numbers()
Numbers = Table.grid()
Numbers.add_column(justify="center")
Numbers.add_row(headers)
Numbers.add_row(numbers)
Number = Panel.fit(
    Numbers,
    box=box.ROUNDED,
    padding=(0, 0),
    border_style="color6",
)
# & ──────────────── table trades ──────────────── #
trades = Table(box=box.SIMPLE_HEAVY, style="color9", padding=(0, 1), expand=True)
get_trades(accs[0], accs[1])
Trades = Panel.fit(
    trades,
    box=box.ROUNDED,
    padding=(1, 2),
    border_style="color9",
)
# & ──────────────── main display ──────────────── #
display_down = Table.grid(padding=0, expand=True, pad_edge=False)
display_down.add_column(justify="right", vertical="middle")
display_down.add_column(justify="right", vertical="middle")
display_down.add_column(justify="right", vertical="middle")
display_down.add_row(Stars, Stats, Trades)
display = Table.grid(padding=0, expand=True, pad_edge=True, collapse_padding=False)
display.add_column(justify="full", vertical="middle")
display.add_row(About)
display.add_row(display_down)
display.add_row(emoji_table)
Display = Panel.fit(
    display,
    box=box.ROUNDED,
    padding=(2, 1),
    title="[color6 b]About the Board Kings' album :rabbit::carrot:",
    subtitle=f"[color6 b]Released at {album['date']}",
    border_style="color6",
)
# !% ──────────────────────────────────────────────────────────── END DISPLAY ─────
# % ─── RUN ────────────────────────────────────────────────────────────────── ✰ ─
update_all()
console.print(Display, justify="center")
if Confirm.ask("[color0]Show the cards [i]by number[/i]?", default=False):
    console.print(Number, justify="center")
else:
    console.print("Ok :wave:")
if Confirm.ask("Update the [i]data[/i]?", default=False):
    ask_account()
elif Confirm.ask("Reset the data?", default=False):
    title = Prompt.ask("Insert the Album Title")
    date = Prompt.ask("Insert the release Date")
    album["title"]=title
    album["date"]=date
    sets = Prompt.ask("Insert title of each set, separated by a comma")
    
    sets_names = sets.split(",")
    if len(sets_names) != 12:
        print("[b] :pile_of_poo: [prompt.invalid]You must enter 12 numbers.")
    else: 
        for x, name in enumerate(sets_names):
            album["sets"][x]["title"] = name
    reset_all()
else:
    print("[b]OK :loudly_crying_face:")

# !% ──────────────────────────────────────────────────────────────── END RUN ─────
