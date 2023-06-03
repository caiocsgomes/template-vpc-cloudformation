# template-vpc-cloudformation


```bash
aws cloudformation create-stack --stack-name vpc --template-body file://vpc.yaml --parameters file://parameters.json
aws cloudformation describe-stack-resources --stack-name vpc
aws cloudformation describe-stack-events --stack-name vpc
aws cloudformation update-stack --stack-name vpc --template-body file://vpc.yaml --parameters file://parameters.json
aws cloudformation wait stack-delete-complete --stack-name MyStack
```

## References

- https://jodies.de/ipcalc