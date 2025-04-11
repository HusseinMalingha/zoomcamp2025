variable "credentials" {
    description = "Project credentials"
    default = file("./keys/my-creds.json")
}

variable "project" {
    description = "Project"
    default = "awesome-ripsaw-373013"
}

variable "location" {
    description = "Project Location"
    default = "asia-south1"
}

variable "bq_dataset_name" {
    description = "Big Query Dataset name"
    default = "example_dataset"
}

variable "gcs_class_name" {
    description = "Class Name"
    default = "STANDARD"
}

variable "gcs_bucket_name" {
    description = "Bucket Name"
    default = "awesome-ripsaw-373013-terra-bucket"
}