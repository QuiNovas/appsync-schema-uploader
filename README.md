# app-schema-uploader

####A command line tool for uploading GraphQL schemas into AWS AppSyncL

This is intended to be used in a CI/CD process for managing AppSync schemas

###Usage
```
python -m appsync_schema_uploader --aws-access-key-id accesskey --aws-secret-access-key secret --aws_region region --api-id id --schema schema.graphql
```

###Arguments
- **aws-access-key-id** The AWS Access Key ID for the IAM user
- **aws-secret-access-key** The AWS Secret Access Key for the IAM user
- **aws-region** The AWS Region of the AppSync API to update
- **api-id** The API ID of the AppSync API to upload the schema to
- **schema** The filename of the SDL formatted schema to upload
 