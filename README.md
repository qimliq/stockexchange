Stock Exchange Simulator Project
--------------------------------
This project has been created to simulate an imaginary Stock exchange, where the investors can buy or sell stocks.

Initially Investor, Broker, Exchange and BookKeeper classes has been implemented. Currently each object created from these classes are using threads and message queues to pass necessary Buy/Sell/Edit/Cancel order messages. 

My plan is to add additional components to run on distributed systems and use RabbitMQ for passing orders to each other in order to make it look like more Real Stock Exchanges.

Despite the significant amount of latency in order message distribution and handling, this project can be used as a baseline for crypto currency exchange implementations.


