# Cloud Provider Capability Map

Use this as a candidate capability map. Treat entries as architectural candidates, not exact one-to-one replacements.

| Logical capability | Azure candidate | AWS candidate | GCP candidate |
|---|---|---|---|
| Global edge entry | Azure Front Door | CloudFront plus Global Accelerator when needed | Cloud Load Balancing plus Cloud CDN |
| CDN / edge caching | Azure CDN / Front Door caching | CloudFront | Cloud CDN |
| API gateway / API management | Azure API Management | Amazon API Gateway | Apigee / API Gateway |
| Container registry | Azure Container Registry | Amazon ECR | Artifact Registry |
| Kubernetes runtime | Azure Kubernetes Service | Amazon EKS | Google Kubernetes Engine |
| Container runtime | Azure Container Apps / AKS | ECS / EKS | Cloud Run / GKE |
| Serverless runtime | Azure Functions | AWS Lambda | Cloud Functions / Cloud Run |
| Relational database | Azure SQL Database | Amazon RDS / Aurora | Cloud SQL / Spanner |
| Document NoSQL | Cosmos DB Core or MongoDB API | DynamoDB / DocumentDB | Firestore |
| Key-value NoSQL | Cosmos DB Core | DynamoDB | Firestore / Bigtable |
| Wide-column NoSQL | Cosmos DB Cassandra API | Keyspaces / DynamoDB depending on model | Bigtable |
| Graph database | Cosmos DB Gremlin API | Neptune | graph pattern via partner or adapted service |
| Cache | Azure Cache for Redis | ElastiCache / MemoryDB | Memorystore |
| Object/blob storage | Azure Storage Account | Amazon S3 | Cloud Storage |
| Event routing | Event Grid | EventBridge | Eventarc / Pub/Sub |
| Event streaming | Event Hubs | Kinesis / MSK | Pub/Sub / Dataflow |
| Private connectivity | ExpressRoute / VPN | Direct Connect / VPN / PrivateLink | Cloud Interconnect / VPN / Private Service Connect |
| Observability | Azure Monitor / App Insights | CloudWatch / X-Ray | Cloud Monitoring / Cloud Trace |
| Identity | Microsoft Entra ID / Managed Identity | IAM / Cognito | IAM / Identity Platform |
| Data lake | ADLS Gen2 | S3 | Cloud Storage |
| Analytical processing | Synapse / Databricks / Fabric | Athena / Glue / EMR / Redshift | BigQuery / Dataflow / Dataproc |
