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
    if f"name_{id}" in session:
        name = session[f"name_{id}"]
        firstfetch = index = flag1 = money = date1 = rupees = category = note = mode = totali = totale = balance =year=month=day= 0
        date2 = []

        if request.method == 'POST':

            data = request.form

            if data['flag'] == 'income' or data['flag'] == 'expense':

                Type = data['flag']
                date1 = data["date"]
                year, month, day = map(int, date1.split('-'))
                print(year,month,day)
                amounts = int(data["rupees"])
                category = data["category"]
                mode = data["mode"]
                note = data["note"]

                if Type == 'income':
                    sendata = supabase.table("data").insert(
                        {"id": id, "Type": Type, "Date": date1, "Amounts": amounts, "Category": category, "Mode": mode,
                         "Note": note, "income": amounts, "expense": 0}).execute()
                if Type == 'expense':
                    sendata = supabase.table("data").insert(
                        {"id": id, "Type": Type, "Date": date1, "Amounts": amounts, "Category": category, "Mode": mode,
                         "Note": note, "income": 0, "expense": amounts}).execute()

            else:
                index = int(data['flag'])
                supabase.table("data").delete().eq("hello", index).execute()

        firstfetch = supabase.table("data").select("*").eq("id", id).execute().data
        finaldata = sorted(firstfetch, key=lambda x: x['Date'])
        print(finaldata)

        fetchincome = supabase.table("data").select("income").eq("id", id).execute().data
        for items in fetchincome:
            totali += items['income']
        print(totali)

        fetchexpense = supabase.table("data").select("expense").eq("id", id).execute().data
        for items in fetchexpense:
            totale += items['expense']
        print(totale)
        dates = {}
        balance = totali + (-totale)
        for entry in finaldata:
            date = entry["Date"]
            if date not in dates:
                dates[date] = []
            year, month, day = map(int, entry['Date'].split('-'))
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
                    "year": year,
                    "month":month,
                    "day":day,

                }
            )

        return render_template('home.html', type=money, date=date1, rupees=rupees, mode=mode, category=category,
                               note=note, dates=dates,
                               finaldata=finaldata, totali=totali, totale=totale, balance=balance, name=name, id=id,
                               year=year, month=month, day=day)
    else:
        return redirect(url_for("home", id=id))


@app.route('/finbot/<id>')
def finbot(id):
    passdata = supabase.table("data").select("*").eq("id", id).execute().data
    return render_template("ChatBot.html", id=id, passdata=passdata)


@app.route('/home')
def home_alternate():
    return redirect(url_for('login'))


@app.route('/graph/<id>', methods=["GET", "POST"])
def graph(id):
    user_year = 0
    user_month = 0
    date = [user_year, user_month]
    if request.method == 'POST':
        user_year = request.form['years']
        user_month = request.form['months']

    Other_ex = Education = Health = Social_life = Transport = Apparel = Food = Household = Allowance = Salary = Bonus = Other = 0
    income_cat = supabase.table("data").select("Category", "Amounts", "Date").eq("id", id).execute().data

    from collections import defaultdict

    category_totals = defaultdict(int)
    print(income_cat)

    print("hi")
    variables_dict = {
        'Other_ex': 0,
        'Education': 0,
        'Health': 0,
        'Social_life': 0,
        'Transport': 0,
        'Apparel': 0,
        'Food': 0,
        'Household': 0,
        'Allowance': 0,
        'Salary': 0,
        'Bonus': 0,
        'Other': 0
    }
    getkey = variables_dict.keys()

    # Iterate through data and aggregate amounts for each category
    for item in income_cat:
        if item['Date'].startswith(f'{user_year}-0{user_month}'):
            category_totals[item['Category']] += int(item['Amounts'])

    # Convert category_totals to a list of dictionaries
    result = [{'Category': category, 'TotalAmount': total} for category, total in category_totals.items()]

    for items in result:
        if items["Category"] == "OTHER_EX":
            Other_ex = items["TotalAmount"]

        elif items["Category"] == "EDUCATION":
            Education = items["TotalAmount"]

        elif items["Category"] == "HEALTH":
            Health = items["TotalAmount"]

        elif items["Category"] == "SOCIAL_LIFE":
            Social_life = items["TotalAmount"]

        elif items["Category"] == "TRANSPORT":
            Transport = items["TotalAmount"]

        elif items["Category"] == "APPAREL":
            Apparel = items["TotalAmount"]

        elif items["Category"] == "FOOD":
            Food = items["TotalAmount"]

        elif items["Category"] == "HOUSEHOLD":
            Household = items["TotalAmount"]

        elif items["Category"] == "ALLOWANCE":
            Allowance = items["TotalAmount"]

        elif items["Category"] == "SALARY":
            Salary = items["TotalAmount"]

        elif items["Category"] == "BONUS":
            Bonus = items["TotalAmount"]

        elif items["Category"] == "OTHER":
            Other = items["TotalAmount"]
        else:
            print("error")

    date_data = supabase.table("data").select("Date", "Type", "Amounts").eq("id", id).execute().data
    week1 = week2 = week3 = week4 = year = month1 = month2 = month3 = month4 = month5 = month6 = month7 = month8 = month9 = month10 = month11 = month12 = day = 0

    from collections import defaultdict

    # Sample data (replace with your actual data retrieval mechanism)
    date_data = [{'Date': '2024-04-01', 'Type': 'income', 'Amounts': '60000'},
                 {'Date': '2024-04-17', 'Type': 'expense', 'Amounts': '7000'},
                 {'Date': '2024-04-01', 'Type': 'expense', 'Amounts': '700'}]

    # Initialize defaultdicts to store income and expense data
    income_data = defaultdict(int)
    expense_data = defaultdict(int)

    # Process date data
    for entry in date_data:
        year, month, day = map(int, entry['Date'].split('-'))
        week = (day - 1) // 7 + 1

        if entry['Type'] == 'income':
            income_data[(year, month, week)] += int(entry['Amounts'])
        elif entry['Type'] == 'expense':
            expense_data[(year, month, week)] += int(entry['Amounts'])

    # Combine income and expense data into final_data
    final_data = []
    for (year, month, week), total_income in income_data.items():
        final_data.append({'Year': year, 'Month': month, 'Week': week, 'Income': total_income, 'Expense': 0})

    for (year, month, week), total_expense in expense_data.items():
        # Check if the entry already exists in final_data, if yes, update the expense
        for item in final_data:
            if item['Year'] == year and item['Month'] == month and item['Week'] == week:
                item['Expense'] = total_expense
                break
        # If the entry doesn't exist, add a new entry for expense
        else:
            final_data.append({'Year': year, 'Month': month, 'Week': week, 'Income': 0, 'Expense': total_expense})

    # Filter data for a specific month

    filtered_data = [item for item in final_data if item['Year'] == int(user_year) and item['Month'] == int(user_month)]

    print(filtered_data)
    # Separate income and expense per week

    income_per_week = [0, 0, 0, 0]
    expense_per_week = [0, 0, 0, 0]
    for item in filtered_data:
        if item['Income']:
            if item['Week'] == 1:
                income_per_week[0] = item['Income']
            if item['Week'] == 2:
                income_per_week[1] = item['Income']
            if item['Week'] == 3:
                income_per_week[2] = item['Income']
            if item['Week'] == 4:
                income_per_week[3] = item['Income']
        if item['Expense']:
            if item['Week'] == 1:
                expense_per_week[0] = item['Expense']
            if item['Week'] == 2:
                expense_per_week[1] = item['Expense']
            if item['Week'] == 3:
                expense_per_week[2] = item['Expense']
            if item['Week'] == 4:
                expense_per_week[3] = item['Expense']

    # Print or process the income and expense data as needed
    print("Income per week:", income_per_week)
    print("Expense per week:", expense_per_week)

    print(income_per_week, expense_per_week)
    # for week, (income, expense) in enumerate(zip(income_per_week, expense_per_week), start=1):
    #     print(f"Week {week}: Income - {income}, Expense - {expense}")

    month = get_month_name(int(user_month))
    print(month)

    return render_template("graph.html", Allowance=Allowance, Bonus=Bonus, Other=Other, Salary=Salary, Health=Health,
                           Household=Household, Food=Food, Apparel=Apparel, Other_ex=Other_ex, Transport=Transport,
                           Social_life=Social_life, Education=Education, income_per_week=income_per_week,
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