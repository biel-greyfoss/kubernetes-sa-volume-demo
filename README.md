# kubernetes-sa-volume-demo

参考 https://learnk8s.io/microservices-authentication-kubernetes


有两个微服务
* api
* data-store

data-store的某些接口只能允许api访问，利用ServiceAccountToken 的卷投射来实现定期刷新的token验证。

具体过程为：
1. api 读取 mount 在 /var/run/secrets/tokens/api-token 位置的token
2. 请求data-store的某些接口时，将该token放入header X-Client-Id中
3. data-store 收到请求时，从header X-Client-Id中读取token
4. 调用V1TokenReview验证token是否有效
5. 若有效，则执行正常业务逻辑，然后返回；否则，返回错误提示


