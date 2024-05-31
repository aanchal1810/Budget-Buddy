# See PyCharm help at https://www.jetbrains.com/help/pycharm/
from flask import Flask, render_template, redirect, request, url_for, session
from supabase import create_client, client
import random
import json

SUPABASE_URL = "https://lmygmmagwjiyhyoggjmq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" \
               ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxteWdtbWFnd2ppeWh5b2dnam1xIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTA5Mzg2Mjc" \
               "sImV4cCI6MjAyNjUxNDYyN30.rcSqf70RtWYFLDBllaiSJh76xPHsB9gMk-93wxc3Fns"

url = SUPABASE_URL
key = SUPABASE_KEY
supabase = create_client(url, key)
app = Flask(__name__)
app.secret_key = "devisgoat"


def generate_id():
    random_digits = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    id_with_prefix = '69' + random_digits
    return id_with_prefix


def get_month_name(month_number):
    months = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }

    return months.get(month_number, "Select Month")


@app.route('/', methods=["GET", "POST"])
def user():
    name = username = email = password = id = 0
    if request.method == 'POST':
        name = request.form["name"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        id = generate_id()
        try:
            supabase.table("users1").insert(
                {"id": id, "Name": name, "username": username, "Email": email, "password": password}).execute()
            supabase.table("data").insert(
                {"id": id}
            ).execute()
            print("hi")
            return redirect(url_for('login'))
        except Exception as e:
            error_message = "An error occurred while signing up. Please try again later."
            return render_template('Register.html', error=error_message)

    return render_template('Register.html', name=name, password=password, email=email, username=username, id=id)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        userid_query = supabase.table("users1").select("id").eq("username", username).execute()
        if userid_query.data:
            userid = userid_query.data[0]['id']
            checkpass_query = supabase.table("users1").select("id, Name").eq("password", password).eq("id",
                                                                                                      userid).execute()
            if checkpass_query.data:
                session[f"name_{userid}"] = checkpass_query.data[0]['Name']
                session[f"userid_{userid}"] = userid  # Set session variables for the logged-in user
                return redirect(url_for('dashboard', id=userid))
    return render_template('login.html')


@app.route('/dashboard/<id>')
def dashboard(id):
    return render_template('homepage.html', id=id)


@app.route('/home/<id>', methods=["GET", "POST"])
def home(id):
    try:
        if f"name_{id}" in session:
            name = session[f"name_{id}"]
            firstfetch = index = flag1 = money = date1 = rupees = category = note = mode = totali = totale = balance =year=month=day= 0
            date2 = []

            if request.method == 'POST':
                data = request.form
                if 'flag' in data and (data['flag'] == 'income' or data['flag'] == 'expense'):
                    Type = data['flag']
                    date1 = data["date"]
                    year, month, day = map(int, date1.split('-'))
                    amounts = int(data["rupees"])
                    category = data["category"]
                    mode = data["mode"]
                    note = data["note"]

                    if Type == 'income':
                        sendata = supabase.table("data").insert(
                            {"id": id, "Type": Type, "Date": date1, "Amounts": amounts, "Category": category, "Mode": mode,
                             "Note": note, "income": amounts, "expense": 0}).execute()
                    elif Type == 'expense':
                        sendata = supabase.table("data").insert(
                            {"id": id, "Type": Type, "Date": date1, "Amounts": amounts, "Category": category, "Mode": mode,
                             "Note": note, "income": 0, "expense": amounts}).execute()

                elif 'flag' in data:
                    index = int(data['flag'])
                    supabase.table("data").delete().eq("hello", index).execute()

            firstfetch = supabase.table("data").select("*").eq("id", id).execute().data
            if firstfetch:
                finaldata = sorted(firstfetch, key=lambda x: x['Date'])
            else:
                finaldata = []

            fetchincome = supabase.table("data").select("income").eq("id", id).execute().data
            for items in fetchincome:
                totali += items.get('income', 0)

            fetchexpense = supabase.table("data").select("expense").eq("id", id).execute().data
            for items in fetchexpense:
                totale += items.get('expense', 0)

            dates = {}
            balance = totali - totale
            for entry in finaldata:
                date = entry["Date"]
                if date not in dates:
                    dates[date] = []
                dates[date].append(
                    {
                        "id": entry["id"],
                        "Date": entry["Date"],
                        "Type": entry["Type"],
                        "Amounts": entry["Amounts"],
                        "Category": entry["Category"],
                        "Mode": entry["Mode"],
                        "Note": entry["Note"],
                        "hello": entry["hello"],
                        "income": entry["income"],
                        "expense": entry["expense"],
                    }
                )

            return render_template('home.html', type=money, date=date1, rupees=rupees, mode=mode, category=category,
                                   note=note, dates=dates,
                                   finaldata=finaldata, totali=totali, totale=totale, balance=balance, name=name, id=id,
                                   year=year, month=month, day=day)
        else:
            return redirect(url_for("home", id=id))
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error: {e}")
        return "An error occurred", 500



@app.route('/finbot/<id>')
def finbot(id):
    passdata = supabase.table("data").select("*").eq("id", id).execute().data
    return render_template("ChatBot.html", id=id, passdata=passdata)


@app.route('/home')
def home_alternate():
    return redirect(url_for('login'))


@app.route('/graph/<id>', methods=["GET", "POST"])
def graph(id):
    user_year = request.form.get('years', 0)
    user_month = request.form.get('months', 0)
    date = [user_year, user_month]

    income_cat = supabase.table("data").select("Category", "Amounts", "Date").eq("id", id).execute().data

    from collections import defaultdict
    category_totals = defaultdict(int)

    for item in income_cat:
        if item['Date'].startswith(f'{user_year}-0{user_month}'):
            category_totals[item['Category']] += int(item['Amounts'])

    result = [{'Category': category, 'TotalAmount': total} for category, total in category_totals.items()]

    data_map = {
        "OTHER_EX": "Other_ex",
        "EDUCATION": "Education",
        "HEALTH": "Health",
        "SOCIAL_LIFE": "Social_life",
        "TRANSPORT": "Transport",
        "APPAREL": "Apparel",
        "FOOD": "Food",
        "HOUSEHOLD": "Household",
        "ALLOWANCE": "Allowance",
        "SALARY": "Salary",
        "BONUS": "Bonus",
        "OTHER": "Other"
    }

    # Initialize all variables to 0
    vars_dict = {v: 0 for v in data_map.values()}

    for items in result:
        if items["Category"] in data_map:
            vars_dict[data_map[items["Category"]]] = items["TotalAmount"]

    date_data = supabase.table("data").select("Date", "Type", "Amounts").eq("id", id).execute().data

    income_data = defaultdict(int)
    expense_data = defaultdict(int)

    for entry in date_data:
        year, month, day = map(int, entry['Date'].split('-'))
        week = (day - 1) // 7 + 1

        if entry['Type'] == 'income':
            income_data[(year, month, week)] += int(entry['Amounts'])
        elif entry['Type'] == 'expense':
            expense_data[(year, month, week)] += int(entry['Amounts'])

    final_data = []
    for (year, month, week), total_income in income_data.items():
        final_data.append({'Year': year, 'Month': month, 'Week': week, 'Income': total_income, 'Expense': 0})

    for (year, month, week), total_expense in expense_data.items():
        for item in final_data:
            if item['Year'] == year and item['Month'] == month and item['Week'] == week:
                item['Expense'] = total_expense
                break
        else:
            final_data.append({'Year': year, 'Month': month, 'Week': week, 'Income': 0, 'Expense': total_expense})

    filtered_data = [item for item in final_data if item['Year'] == int(user_year) and item['Month'] == int(user_month)]

    income_per_week = [0, 0, 0, 0]
    expense_per_week = [0, 0, 0, 0]
    for item in filtered_data:
        if item['Income']:
            income_per_week[item['Week'] - 1] = item['Income']
        if item['Expense']:
            expense_per_week[item['Week'] - 1] = item['Expense']

    month = get_month_name(int(user_month))

    return render_template("graph.html", Allowance=vars_dict['Allowance'], Bonus=vars_dict['Bonus'], Other=vars_dict['Other'], Salary=vars_dict['Salary'], Health=vars_dict['Health'],
                           Household=vars_dict['Household'], Food=vars_dict['Food'], Apparel=vars_dict['Apparel'], Other_ex=vars_dict['Other_ex'], Transport=vars_dict['Transport'],
                           Social_life=vars_dict['Social_life'], Education=vars_dict['Education'], income_per_week=income_per_week,
                           expense_per_week=expense_per_week, date=date, month=month, id=id)



@app.route('/cal/<id>')
def cal(id):
    Type = amount = note = date = 0
    events = []
    fetch = supabase.table("data").select("*").eq("id", id).execute().data
    data = sorted(fetch, key=lambda x: x['Date'])
    for items in data:
        Type = items['Type']
        date = items['Date']
        amount = items['Amounts']
        note = items['Note']
        end = ''
        if Type == 'income':
            events.append({'title': note, 'start': date, 'end': end, 'color': 'green', 'rupees': amount})
        if Type == 'expense':
            events.append({'title': note, 'start': date, 'end': end, 'color': 'red', 'rupees': amount})

    print(events)

    return render_template("cal.html", events=events, id=id, Type=type, amount=amount, note=note)


@app.route('/logout/<id>')
def logout(id):
    session.pop(f"name_{id}", None)  # Remove username from session
    session.pop(f"userid_{id}", None)  # Remove userid from session

    # Redirect user to the login page after logout
    return redirect(url_for("login", id=id))


@app.route('/aboutus/<id>')
def aboutus(id):
    return render_template("aboutus.html", id=id)


if __name__ == '__main__':
    app.run(debug=True, port=1100)

data = \
    {
        'year': 2024,
        'months':
            [
                {
                    'January': {
                        'week1': 200,
                        'week2': 700,
                        'week3': 500,
                        'week4': 600
                    },
                    'February': {
                        'week1': 200,
                        'week2': 700,
                        'week3': 500,
                        'week4': 600
                    }
                }
            ]
    }
