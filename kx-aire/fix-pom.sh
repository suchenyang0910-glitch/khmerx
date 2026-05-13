# 修复 auth-service pom.xml - 添加 repackage 目标
sed -i '/<\/configuration>/a                <executions>                    <execution>                        <goals>                            <goal>repackage</goal>                        </goals>                    </execution>                </executions>' auth-service/pom.xml

# 修复 risk-engine-service pom.xml
sed -i '/<\/configuration>/a                <executions>                    <execution>                        <goals>                            <goal>repackage</goal>                        </goals>                    </execution>                </executions>' risk-engine-service/pom.xml
