# SPL211: Covid Vaccine Distribution Center

## Python and SQL
## compiled on Ubuntu 18.04.1 LTS

```
Responsible TA:Or Dinari
Due Date:17/1/2021 23:
```
## 1 Introduction

In this assignment you are required to implement the database of aSARS-CoV-2vaccine distribution center.
The assignment is composed of three parts:

1. Create and populate the database according to a configuration file.
2. Execute a list of orders, according to a second file.
3. Print a summary in a third file.

## 2 Building the Database

You will store the database file at database.db.
The database will contain the following tables:

## 2.1 Structure

- vaccines: Hold the information on the vaccines currently in the inventory.
    - id INTEGER PRIMARY KEY
    - date DATE NOT NULL
    - supplier INTEGER REFERENCES Supplier(id)
    - quantity INTEGER NOT NULL
- suppliers: Holds the suppliers data.


- id INTEGER PRIMARY KEY
- name STRING NOT NULL
- logistic INTEGER REFERENCES Logistic(id)
- clinics: Holds the information on the different clinics.
- id INTEGER PRIMARY KEY
- location STRING NOT NULL
- demand INTEGER NOT NULL
- logistic INTEGER REFERENCES Logistic(id)
- logistics: Holds the information on the different delivery services.
- id INTEGER PRIMARY KEY
- name STRING NOT NULL
- count_sent INTEGER NOT NULL
- count_received INTEGER NOT NULL

### 2.2 Configuration file

In order to build the database, you will parse a configuration file, the file will have the following structure:

<#1>,<#2>,<#3>,<#4>
<vaccines>
<suppliers>
<clinics>
<logistics>

Where each of the numbers in the first line stands for the number of entries of that type, and each entry has
the relevant table details, separated by a comma. For example:

3,1,2,
1,2021-01-10,1,
2,2021-01-11,1,
3,2021-01-12,1,
1,Pfizer,
1,Beer-Sheva,50,
2,Tel-Aviv,150,
1,DHL,0,
2,UPS,0,

In the above example we have 3 bulks of vaccines in the inventory, 1 supplier, 2 clinics, and 2 logistics
services. Note that there are no spaces, just comas and new lines.

## 3 Orders

You will support two type of orders:

receive_shipment This order will receive a shipment from one of the available suppliers:

<name>,<amount>,<date>

This order will add< amount >vaccines from< name >on< date >. Executing the order will add the
relevant item to the Vaccines table, and update the count_received on the relevant supplier. For example,
using the previous example tables:

Pfizer,20,2021-01-

Will add an entry in the Vaccines table, with4,2021-01-02,1,20, and increase the count_received by 20 on
the DHL entry.

send_shipment This order will send a shipment from the distribution center to one of the clinics:

<location>,<amount>

This order will remove< amount >from the demand of< location >, in addition, it will remove the sum of
< amount >from the inventory, if the quantity of an entry in the Vaccines table reduce to zero, that entry
should be removed from the table. Note that if< amount >is larger than a single entry, the order will
affect multiple entries. Older vaccines will be shipped prior to newer ones. In a similar way to the previous
order, we will update the relevant logistic service count_sent with the added< amount >. For example,
using the previous example tables:

Tel-Aviv,

Will reduce the demand in Tel-Aviv by 50, remove all three entries from the Vaccines table, and increase
the count_sent by 50 on the DHL UPS entry.

### 3.1 Executing the Orders

The orders will be read from the specified file, and executed in the order they appear in the file, each line
will be a single order. For example:

Pfizer,20,2021-01-
Pfizer,100,2021-01-
Tel-Aviv,

Will first receive the two shipments from Pfizer, then send a single shipment to Tel-Aviv.

## 4 Summary File

After each order a line will be added to the summary, the line should include:

<total_inventory>,<total_demand>,<total_received>,<total_sent>

For executing the 3 orders above, using the previous table, you will have an output file of 3 lines:

70,200,20,
170,200,120,
130,160,120,
