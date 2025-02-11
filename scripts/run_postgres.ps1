# ---------------------------
# PostgreSQL Variables
# ---------------------------
$pgContainerName   = "my-postgres"
$pgUser            = "myuser"
$pgPassword        = "mypassword"
$pgDB              = "mydatabase"
$pgHostPort        = 5432
$pgContainerPort   = 5432
$pgImage           = "postgres:latest"

# ---------------------------
# RabbitMQ Variables
# (Using the "3-management" tag for mgmt console on 15672)
# ---------------------------
$rmqContainerName  = "my-rabbit"
$rmqImage          = "rabbitmq:3-management"
$rmqHostPortAMQP   = 5672      # AMQP port
$rmqHostPortMgmt   = 15672     # RabbitMQ Management UI
$rmqContainerPortAMQP = 5672
$rmqContainerPortMgmt = 15672

# ---------------------------
# Function to stop/remove container if it exists
# ---------------------------
function Remove-ExistingContainerIfAny($containerName) {
    $existingContainer = docker ps -a --filter "name=$containerName" --format "{{.Names}}"
    if ($existingContainer -eq $containerName) {
        Write-Host "Container $containerName already exists. Stopping and removing it..."
        docker stop $containerName | Out-Null
        docker rm $containerName | Out-Null
    }
}

# ---------------------------
# 1) Start PostgreSQL Container
# ---------------------------
Remove-ExistingContainerIfAny $pgContainerName

# Build the port mapping string for PostgreSQL
$pgPortMapping = "$($pgHostPort):$($pgContainerPort)"

Write-Host "Starting PostgreSQL container: $pgContainerName ..."
docker run -d --name $pgContainerName `
    -p $pgPortMapping `
    -e "POSTGRES_USER=$pgUser" `
    -e "POSTGRES_PASSWORD=$pgPassword" `
    -e "POSTGRES_DB=$pgDB" `
    $pgImage | Out-Null

Write-Host "PostgreSQL container '$pgContainerName' is running on port $pgHostPort."

# ---------------------------
# 2) Start RabbitMQ Container
# ---------------------------
Remove-ExistingContainerIfAny $rmqContainerName

# Build port mappings for RabbitMQ
$rmqPortMappingAMQP = "$($rmqHostPortAMQP):$($rmqContainerPortAMQP)"
$rmqPortMappingMgmt = "$($rmqHostPortMgmt):$($rmqContainerPortMgmt)"

Write-Host "Starting RabbitMQ container: $rmqContainerName ..."
docker run -d --name $rmqContainerName `
    -p $rmqPortMappingAMQP `
    -p $rmqPortMappingMgmt `
    $rmqImage | Out-Null

Write-Host "RabbitMQ container '$rmqContainerName' is running on ports $rmqHostPortAMQP (AMQP) and $rmqHostPortMgmt (Mgmt UI)."
Write-Host "You can access the RabbitMQ management UI at: http://localhost:$rmqHostPortMgmt"
