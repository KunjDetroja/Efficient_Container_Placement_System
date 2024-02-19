# Efficient Container Placement System 
Overview:

A Yard Management System (YMS) is a software solution that INTECH has developed and is used in logistics and supply chain management to efficiently manage the movement and storage of goods within a yard or facility. A yard typically refers to an area within a distribution center, manufacturing plant, or transportation hub where containers, trailers, and other assets are stored temporarily before being loaded, unloaded, or transferred.

Containers are standardized units used for transporting goods, often made of metal or other materials, designed to be easily handled by various modes of transportation, such as ships, trucks, and trains. These containers can vary in size (typically 20ft and 40 ft) and types, such as refrigerated containers or reefer containers, which is a specialized type of shipping container designed to transport goods that require temperature-controlled environments such as vegetables, fruits, dairy products, etc.

A YMS helps organizations to streamline operations by providing real-time visibility into yard activities, tracking the location of containers and trailers, optimizing the movement of assets, and coordinating tasks such as loading, unloading, and transshipment. This enhances efficiency, reduces delays, and minimizes congestion in the yard, ultimately improving the overall supply chain process.

# Problem Statement
The goal of this project is to develop an AI-powered system that will guide and place the incoming containers in an optimized way such that there will be less shuffling and the best way to place containers. Container placement must be done within a short period. The system should be able to provide relevant and accurate locations with containers.
The proposed solution must consider the following things

●	 Containers must be segregated by their size like 20ft and 40ft.
  
  ○	In a given row and bay all levels must be the same container size. 
  
●	Locations are specific for Import, Export, and Empty containers. The system must identify the places and put those containers there.

●	All possible locations must be taken in such a way that less shuffling must occur while taking out containers.

●	If anyhow the system assigns the location that is at the higher level but lower levels are empty, the location must get updated. In short, no location must be suggested which is in the air. 

# ECPS System Responsibility:
●	Predict the timing of the individual containers: The system must be able to predict the leave time of the containers.

●	Generate the optimized location of an individual container: Based on leave time our system must place the containers in an optimized way such that it leads to less shuffling while carrying out outgoing operation.

●	Scale to handle large volumes of containers: The system should be able to handle large volumes of containers without compromising on performance or quality of responses.
