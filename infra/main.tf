provider "google" {
  project = "jiit-data"
}

terraform {
  backend "gcs" {
    bucket  = "jjit-data-tfstate"
    prefix  = "spotify-recommender"
  }
}

variable "region" {
  default = "europe-central2"
}

variable "zone" {
  default = "europe-central2-a"
}

resource "google_compute_network" "spotify-vpc-net" {
  name                    = "spotify-recommender-net"
  auto_create_subnetworks = false
  mtu                     = 1460
}

resource "google_compute_subnetwork" "spotify-subnet" {
  name          = "spotify-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.region
  network       = google_compute_network.spotify-vpc-net.id
}

# Create a single Compute Engine instance
resource "google_compute_instance" "default" {
  name         = "spotify-vm"
  machine_type = "n1-standard-4	"
  zone         = var.zone
  tags         = ["ssh"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  metadata_startup_script = file("./startup.sh")

  network_interface {
    subnetwork = google_compute_subnetwork.spotify-subnet.id

    access_config {
      # Include this section to give the VM an external IP address
    }
  }
}

resource "google_compute_firewall" "ssh" {
  name = "allow-ssh"
  allow {
    ports    = ["22"]
    protocol = "tcp"
  }
  direction     = "INGRESS"
  network       = google_compute_network.spotify-vpc-net.id
  priority      = 1000
  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["ssh"]
}

resource "google_compute_firewall" "app" {
  name    = "spotify-app-firewall"
  network = google_compute_network.spotify-vpc-net.id

  allow {
    protocol = "tcp"
    ports    = ["8000"]
  }
  source_ranges = ["0.0.0.0/0"]
}

output "spotify-url" {
 value = join("",["http://",google_compute_instance.default.network_interface.0.access_config.0.nat_ip,":8000"])
}