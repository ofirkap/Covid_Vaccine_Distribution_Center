from persistance_layer import repo, Vaccine, Supplier, Clinic, Logistic
import sys
import atexit

total_inventory = 0
total_demand = 0
total_received = 0
total_sent = 0


# adds the data from the config_file to the database
# adds logistics first, then clinics, suppliers and lastly vaccines to correctly insert all references
def config_database(path):
    global total_inventory
    global total_demand
    with open(path, encoding='utf8') as input_file:

        line = input_file.readline().rstrip('\n')
        sizes = list(map(int, line.split(',')))
        config_list = input_file.read().splitlines()

        current_index = sum(sizes) - sizes[3]
        for i in range(current_index, current_index + sizes[3]):
            repo.logistics.insert(Logistic(*config_list[i].split(',')))

        current_index -= sizes[2]
        for i in range(current_index, current_index + sizes[2]):
            clinic = Clinic(*config_list[i].split(','))
            total_demand += int(clinic.demand)
            repo.clinics.insert(clinic)

        current_index -= sizes[1]
        for i in range(current_index, current_index + sizes[1]):
            repo.suppliers.insert(Supplier(*config_list[i].split(',')))

        for i in range(int(sizes[0])):
            vaccine = Vaccine(*config_list[i].split(','))
            total_inventory += int(vaccine.quantity)
            repo.vaccines.insert(vaccine)


# add a new vaccine to the database and increase the 'total received' count
def receive_shipment(params):
    supplier = repo.suppliers.find(name=params[0])
    repo.vaccines.insert(Vaccine(None, params[2], supplier.id, params[1]))
    repo.logistics.increment('count_received', int(params[1]), supplier.logistic)


# remove vaccines by date until the demand (amount to send) is met
def send_shipment(params):
    demand = int(params[1])
    clinic = repo.clinics.find(location=params[0])
    repo.clinics.increment('demand', -demand, clinic.id)
    logistic = repo.logistics.find(id=clinic.logistic)
    repo.logistics.increment('count_sent', demand, logistic.id)

    while demand > 0:

        vaccine = repo.vaccines.find_first_by_order('date')
        amount = vaccine.quantity

        if amount > demand:
            repo.vaccines.increment('quantity', - demand, vaccine.id)
            demand = 0
        else:
            repo.vaccines.delete(id=vaccine.id)
            demand -= vaccine.quantity


# receive a line and determine whether is its a 'send' or 'receive' order and execute accordingly
def execute_order(line):
    global total_inventory
    global total_demand
    global total_received
    global total_sent
    params = line.split(',')

    if len(params) == 3:
        total_inventory += int(params[1])
        total_received += int(params[1])
        receive_shipment(params)
    else:
        total_inventory -= int(params[1])
        total_demand -= int(params[1])
        total_sent += int(params[1])
        send_shipment(params)


# adds the current stats to the summary file
def add_to_summary(output_file):
    global total_inventory
    global total_demand
    global total_received
    global total_sent
    output_file.write(f"{total_inventory},{total_demand},{total_received},{total_sent}\n")


def main(argv):
    atexit.register(repo._close)
    config_database(argv[1])
    with open(argv[3], 'a') as output_file:
        with open(argv[2], encoding='utf8') as orders:
            line = orders.readline().rstrip('\n')
            while line:
                execute_order(line)
                add_to_summary(output_file)
                line = orders.readline().rstrip('\n')


if __name__ == '__main__':
    main(sys.argv)
