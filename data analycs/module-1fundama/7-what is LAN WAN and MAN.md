# Computer Networks: LAN, WAN, and MAN

## Introduction

A **computer network** is a collection of interconnected devices (computers, servers, printers, smartphones, etc.) that communicate and share resources. Networks are classified based on their geographical coverage, speed, ownership, and purpose.

---

# Types of Computer Networks

1. PAN (Personal Area Network)
2. LAN (Local Area Network)
3. CAN (Campus Area Network)
4. MAN (Metropolitan Area Network)
5. WAN (Wide Area Network)
6. GAN (Global Area Network)

---

# 1. PAN (Personal Area Network)

## Definition

A **Personal Area Network (PAN)** is the smallest type of network. It connects devices within a short range (typically up to 10 meters).

## Features

- Very small coverage area
- Low power consumption
- Easy to set up
- Usually wireless

## Technologies Used

- Bluetooth
- USB
- NFC
- Infrared

## Examples

- Connecting a smartphone to wireless earbuds
- Smartwatch connected to a phone
- Laptop connected to a wireless mouse

## Advantages

- Low cost
- Portable
- Easy installation

## Disadvantages

- Limited range
- Limited number of devices
- Lower speed compared to LAN

---

# 2. LAN (Local Area Network)

## Definition

A **Local Area Network (LAN)** is a network that connects devices within a limited geographical area such as a home, office, laboratory, school, or building.

## Coverage Area

- Few meters to a few kilometers

## Features

- High data transfer speed
- Privately owned
- Low latency
- Easy maintenance

## Technologies Used

- Ethernet
- Wi-Fi
- Fiber Optic
- Switches
- Routers

## Components

- Computers
- Switches
- Routers
- Access Points
- Ethernet Cables

## Advantages

- Fast communication
- Easy file sharing
- Printer sharing
- Internet sharing
- High security

## Disadvantages

- Limited geographical coverage
- Setup cost
- Requires maintenance

## Examples

- Home Wi-Fi network
- School computer lab
- Office network
- Library network

### LAN Diagram

```
        Internet
            |
         Router
            |
        +-------+
        | Switch|
        +-------+
       /    |    \
     PC1   PC2  Printer
```

---

# 3. CAN (Campus Area Network)

## Definition

A **Campus Area Network (CAN)** connects multiple LANs within a campus such as a university, hospital, military base, or company campus.

## Coverage Area

- 1 km to 10 km

## Features

- High-speed communication
- Connects multiple buildings
- Managed by one organization

## Advantages

- Efficient communication
- Resource sharing
- High speed

## Examples

- University campus
- Corporate campus
- Hospital campus

---

# 4. MAN (Metropolitan Area Network)

## Definition

A **Metropolitan Area Network (MAN)** connects multiple LANs across a city or metropolitan area.

## Coverage Area

- 5 km to 50 km (sometimes up to 100 km)

## Features

- Larger than LAN
- Smaller than WAN
- High-speed backbone
- Often managed by ISPs or government organizations

## Technologies Used

- Fiber Optic
- Metro Ethernet
- Microwave Links

## Advantages

- Covers an entire city
- High-speed communication
- Resource sharing between organizations

## Disadvantages

- More expensive than LAN
- Complex management
- Higher maintenance cost

## Examples

- City-wide internet network
- Cable TV network
- Government offices connected across a city
- Bank branches within a city

### MAN Diagram

```
      Office A
         |
      Fiber Network
         |
  --------------------
  |        |         |
Office B Office C Office D
```

---

# 5. WAN (Wide Area Network)

## Definition

A **Wide Area Network (WAN)** connects computers and networks over large geographical distances such as countries or continents.

## Coverage Area

- Hundreds to thousands of kilometers

## Features

- Largest type of network
- Connects multiple MANs and LANs
- Uses leased lines, satellites, fiber optics
- Managed by telecom companies and ISPs

## Technologies Used

- MPLS
- Satellite Communication
- Fiber Optic
- VPN
- Internet

## Advantages

- Global communication
- Connects remote offices
- Centralized data access
- Supports cloud computing

## Disadvantages

- Expensive
- Higher latency
- Complex management
- Security concerns

## Examples

- The Internet
- Banking networks
- Airline reservation systems
- Multinational company networks

### WAN Diagram

```
   City A LAN
        |
      Internet
        |
   City B LAN
        |
   Country C LAN
```

---

# 6. GAN (Global Area Network)

## Definition

A **Global Area Network (GAN)** is a worldwide network that connects multiple WANs across the globe.

The **Internet** is the best example of a GAN.

## Coverage Area

- Worldwide

## Features

- Global connectivity
- Uses satellites and undersea fiber cables
- Connects millions of devices

## Examples

- Internet
- International banking networks
- Global cloud services

---

# Comparison Table

| Feature | PAN | LAN | CAN | MAN | WAN | GAN |
|----------|-----|-----|-----|-----|-----|-----|
| Full Form | Personal Area Network | Local Area Network | Campus Area Network | Metropolitan Area Network | Wide Area Network | Global Area Network |
| Coverage | Up to 10 m | Building | Campus | City | Country/Continent | Worldwide |
| Speed | Low | Very High | High | High | Moderate | Moderate |
| Cost | Low | Low | Medium | High | Very High | Extremely High |
| Ownership | Individual | Private | Organization | ISP/Organization | Telecom Providers | Multiple Providers |
| Example | Bluetooth | Office Network | University Campus | City Network | Internet Backbone | Global Internet |

---

# LAN vs MAN vs WAN

| Feature | LAN | MAN | WAN |
|----------|-----|-----|-----|
| Full Form | Local Area Network | Metropolitan Area Network | Wide Area Network |
| Coverage | Building | City | Country/World |
| Speed | Very High | High | Moderate |
| Cost | Low | Medium | High |
| Ownership | Private | Organization/ISP | Telecom Companies |
| Setup Complexity | Easy | Moderate | Complex |
| Security | High | Medium | Lower |
| Example | Home Wi-Fi | City Network | Internet |

---

# Summary

- **PAN** connects personal devices within a few meters.
- **LAN** connects devices inside a building, office, or school.
- **CAN** connects multiple LANs across a campus.
- **MAN** connects LANs across a city.
- **WAN** connects networks across countries and continents.
- **GAN** connects networks globally, with the Internet being the largest example.

As the coverage area increases from **PAN → LAN → CAN → MAN → WAN → GAN**, the network becomes more complex, more expensive, and generally experiences higher latency.