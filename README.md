# Grafana Demo

This project demonstrates the use of Grafana for data visualization and monitoring. Below is a detailed overview of the repository structure and instructions to get started.

## Project Structure

```
grafana-demo/
├── dashboards/
│   └── sample-dashboard.json
├── docker-compose.yml
├── grafana/
│   └── provisioning/
│       ├── datasources/
│       │   └── datasource.yml
│       └── dashboards/
│           └── dashboard.yml
├── README.md
```

### Key Files and Directories

- **docker-compose.yml**: Docker Compose configuration to run Grafana and related services.
- **grafana/provisioning/**: Contains provisioning files for automatic setup of datasources and dashboards.


## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

### Running Grafana

1. Clone the repository:
     ```sh
     git clone https://github.com/yourusername/grafana-demo.git
     cd grafana-demo
     ```

2. Start the services:
     ```sh
     docker-compose up -d
     ```
