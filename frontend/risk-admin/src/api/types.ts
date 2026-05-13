export type TokenResponse = {
  accessToken: string
  tokenType: string
  expiresInMs: number
}

export type MeResponse = {
  actorId: string
  roles: string[]
  permissions: string[]
}

export type PageResponse<T> = {
  items: T[]
  total: number
  page: number
  pageSize: number
}

export type RiskRule = {
  ruleId: string
  ruleName: string
  scenarioType: string
  ruleExpression: string
  scoreWeight: number
  riskAction: string
  status: number
}

export type RiskEvent = {
  eventId: string
  merchantId: string
  scenarioType: string
  userId: string
  orderId: string
  riskScore: number
  riskLevel: string
  decision: string
  reason: string
  matchedRuleIds: string
  inputSnapshot: string
  status: string
  createdAt: string
  updatedAt: string
}

export type Disposition = {
  dispositionId: string
  eventId: string
  action: string
  remark: string
  operatorId: string
  createdAt: string
}

export type RiskEventDetailResponse = {
  event: RiskEvent | null
  dispositions: Disposition[]
}

export type AuditLog = {
  logId: string
  actorId: string
  action: string
  objectType: string
  objectId: string
  diffJson: string
  ip: string
  userAgent: string
  createdAt: string
}

export type AdminUser = {
  userId: string
  email: string
  displayName: string
  status: number
  createdAt: string
  roleKeys: string[]
}

export type Role = {
  roleId: string
  roleKey: string
  roleName: string
  builtIn: number
  permissionKeys: string[]
}

export type Permission = {
  permKey: string
  permName: string
}
