extern yield_t resolve_dns_address(dnsaddr_t dnsaddr, dqdata_t querydata, sainet_s *resolver, dqtypeclass_t type);
nonyield_t parse_dqflags(dqdata_t querydata, dqflags_s *dst);
nonyield_t parse_dqnumbers(dqdata_t querydata, dqnumbers_s *dst);
nonyield_t parse_dqheader(dqdata_t querydata, dqheader_s *dst);
yield_t parse_dqquestion(dqdata_t querydata, dqquestion_s *dst);
nonyield_t parse_dqrecord(dqdata_t querydata, dqrecord_s *dst);
nonyield_t parse_dnsquery(dqdata_t querydata, dnsquery_s *dst);
yield_t make_dnsquery_and_get_rdata(dnsaddr_t dnsaddr, dnsresolver_t resolver, inetport_t port, dqtypeclass_t type, dqrdata_t dst);
yield_t make_dnsquery_and_get_inetaddr(dnsaddr_t dnsaddr,dnsresolver_t resolver, inetport_t port, inetaddr_t *dst);
yield_t make_dnsquery_and_get_inet6addr(dnsaddr_t dnsaddr,dnsresolver_t resolver, inetport_t port, inet6addr_t *dst);