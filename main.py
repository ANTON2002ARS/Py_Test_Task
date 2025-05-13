import sys
from collections import defaultdict
# разбиваем строку .csv
def parse_line(line):
    return line.strip().split(',')

# сопоставление всех колонок
def find_column(header, possible_names):
    header_lower = [h.lower() for h in header]
    for name in possible_names:
        if name.lower() in header_lower:
            return header_lower.index(name.lower())
    return None

# перебиваем и сортиреуем файлы для
def read_employees(files):
    employees = []
    for filename in files:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # название всех колонок
            header = parse_line(lines[0])
            idx_hours = find_column(header, ['hours_worked', 'hours', 'worked_hours'])
            idx_rate = find_column(header, ['hourly_rate', 'rate', 'salary'])
            idx_department = find_column(header, ['department', 'dept'])
            idx_name = find_column(header, ['name','names'])
            idx_email = find_column(header, ['email','emails'])
            idx_id = find_column(header,['id','ip'])
            if idx_hours is None or idx_rate is None or idx_department is None:
                print(f"Ошибка: в файле {filename} не найдены обязательные колонки для подсчета запрлат сотрудников ")
                sys.exit(1)

            for line in lines[1:]:
                if not line.strip():
                    continue
                values = parse_line(line)
                row = {}
                if idx_id is not None and idx_id < len(values):
                    row['id'] = values[idx_id]
                if idx_email is not None and idx_email < len(values):
                    row['email'] = values[idx_email]
                if idx_name is not None and idx_name < len(values):
                    row['name'] = values[idx_name]
                if idx_department is not None and idx_department < len(values):
                    row['department'] = values[idx_department]

                # Числовые поля
                try:
                    row['hours_worked'] = float(values[idx_hours])
                    row['hourly_rate'] = float(values[idx_rate])
                except (ValueError, IndexError):
                    print(f"Ошибка: неверный формат числовых данных в файле {filename} в строке: {line.strip()}")
                    sys.exit(1)

                employees.append(row)
    return employees

# функции отчетов
def report_payout(employees):
    payouts_by_department = defaultdict(float)
    total_payout = 0.0

    for emp in employees:
        payout = emp['hours_worked'] * emp['hourly_rate']
        payouts_by_department[emp['department']] += payout
        total_payout += payout

    print("Отчёт по зарплатам:")
    for dept, payout in payouts_by_department.items():
        print(f"  Отдел {dept}: {payout:.2f}")
    print(f"Общая сумма выплат: {total_payout:.2f}")

def report_emails(employees):
    print("Список сотрудников (id и email):")
    for emp in employees:
        name = emp.get('name', 'N/A')
        email = emp.get('email', 'N/A')
        print(f" Почта сотрудника по имени {name}: {email}")

def report_id(employees):
    print("Список id все сотрудников :")
    for emp in employees:
        name = emp.get('name', 'N/A')
        emp_id = emp.get('id', 'N/A')
        print(f"id сотрудника по имени {name}: {emp_id}")

# вывод для формата
def print_usage(reports):
    print("Форматы доступных запросов: ")
    print("python script.py data1.csv ... --report payout")
    print("python script.py data1.csv ... --report emails")
    print("python script.py data1.csv ... --report id")
    print("python script.py --help")
    print(f"Доступные отчёты: {', '.join(reports)}")

def main():
    reports = {
        'payout': report_payout,
        'emails': report_emails,
        'id': report_id,
    }
    if "--help" in sys.argv:
        print_usage(reports.keys())
        return

    if len(sys.argv) < 3:
        print_usage(reports.keys())
        return

    try:
        report_index = sys.argv.index('--report')
    except ValueError:
        print_usage(reports.keys())
        return

    files = sys.argv[1:report_index]
    if not files:
        print_usage(reports.keys())
        return

    report_type = sys.argv[report_index + 1] if report_index + 1 < len(sys.argv) else None
    if not report_type:
        print("Ошибка: не указан тип отчёта после --report []")
        print_usage(reports.keys())
        return

    # список из всех полученых файлов
    employees = read_employees(files)
    #print(employees)

    if report_type not in reports:
        print(f"Отчёт '{report_type}' пока не поддерживается.")
        return
    # выполнение отчета из доступных
    reports[report_type](employees)

if __name__ == '__main__':
    main()
