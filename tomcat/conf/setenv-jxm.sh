IPADDR=`/sbin/ifconfig eth0 | grep 'inet '| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'`;
CATALINA_OPTS="$CATALINA_OPTS -Djava.rmi.server.hostname=$IPADDR"
CATALINA_OPTS="$CATALINA_OPTS -Dcom.sun.management.jmxremote.port=30000"
CATALINA_OPTS="$CATALINA_OPTS -Dcom.sun.management.jmxremote.ssl=false"
CATALINA_OPTS="$CATALINA_OPTS -Dcom.sun.management.jmxremote"
CATALINA_OPTS="$CATALINA_OPTS -Dcom.sun.management.jmxremote.authenticate=true"
CATALINA_OPTS="$CATALINA_OPTS -Dcom.sun.management.jmxremote.password.file=/pang/program/jmxtrans/jmx.password"
CATALINA_OPTS="$CATALINA_OPTS -Dcom.sun.management.jmxremote.access.file=/pang/program/jmxtrans/jmx.access"
