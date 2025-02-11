# Variables – adjust these values as needed
$containerName = "my-postgres"
$postgresUser = "myuser"
$postgresPassword = "mypassword"
$postgresDB = "mydatabase"
$hostPort = 5432
$containerPort = 5432
$image = "postgres:latest"

# Check if a container with the given name already exists
$existingContainer = docker ps -a --filter "name=$containerName" --format "{{.Names}}"

if ($existingContainer -eq $containerName) {
    Write-Host "Container $containerName already exists. Stopping and removing it..."
    docker stop $containerName | Out-Null
    docker rm $containerName | Out-Null
}

# Build the port mapping string using subexpression syntax to correctly insert the variables
$portMapping = "$($hostPort):$($containerPort)"

# Run the PostgreSQL container in detached mode with the specified environment variables and port mapping
docker run -d --name $containerName -p $portMapping `
    -e "POSTGRES_USER=$postgresUser" `
    -e "POSTGRES_PASSWORD=$postgresPassword" `
    -e "POSTGRES_DB=$postgresDB" `
    $image

Write-Host "PostgreSQL container '$containerName' is running on port $hostPort."
