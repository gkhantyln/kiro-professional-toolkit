---
name: setup-kubernetes
description: Create production-ready Kubernetes manifests with Deployment, Service, Ingress, HPA, and Helm chart
---

# Setup Kubernetes

Creates complete Kubernetes configuration including:
- Deployment with rolling updates and probes
- Service and Ingress with TLS
- HPA autoscaling
- ConfigMap and Secret management
- Network policies
- Helm chart structure
- Kustomize overlays

## Usage
```
#setup-kubernetes <app-name>
```

## Generated Files

### deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ APP_NAME }}
  labels:
    app: {{ APP_NAME }}
    version: "{{ VERSION }}"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {{ APP_NAME }}
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: {{ APP_NAME }}
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8080"
    spec:
      serviceAccountName: {{ APP_NAME }}
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 2000
      containers:
        - name: {{ APP_NAME }}
          image: {{ IMAGE }}:{{ TAG }}
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
              name: http
          env:
            - name: NODE_ENV
              value: production
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: {{ APP_NAME }}-secrets
                  key: database-url
          envFrom:
            - configMapRef:
                name: {{ APP_NAME }}-config
          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi
          livenessProbe:
            httpGet:
              path: /health/live
              port: http
            initialDelaySeconds: 30
            periodSeconds: 10
            failureThreshold: 3
          readinessProbe:
            httpGet:
              path: /health/ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 5
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop: [ALL]
      topologySpreadConstraints:
        - maxSkew: 1
          topologyKey: kubernetes.io/hostname
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: {{ APP_NAME }}
```

### hpa.yaml
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {{ APP_NAME }}
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {{ APP_NAME }}
  minReplicas: 2
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
    scaleUp:
      stabilizationWindowSeconds: 0
      policies:
        - type: Percent
          value: 100
          periodSeconds: 15
```

### ingress.yaml
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {{ APP_NAME }}
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - {{ DOMAIN }}
      secretName: {{ APP_NAME }}-tls
  rules:
    - host: {{ DOMAIN }}
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: {{ APP_NAME }}
                port:
                  name: http
```

### network-policy.yaml
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: {{ APP_NAME }}
spec:
  podSelector:
    matchLabels:
      app: {{ APP_NAME }}
  policyTypes:
    - Ingress
    - Egress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - port: 8080
  egress:
    - to:
        - namespaceSelector:
            matchLabels:
              name: database
      ports:
        - port: 5432
    - to: []
      ports:
        - port: 53
          protocol: UDP
```
