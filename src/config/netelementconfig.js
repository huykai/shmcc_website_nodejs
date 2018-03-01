var netelements = [ 
    {
      'type' : 'telnet',
      'name' : 'SHMME03BNK',
      'host' : '127.0.0.1',
      'port' : '51004',
      'login': [
        { prompt: 'USERNAME', answer: 'NOKIA1\r' },
        { prompt: 'PASSWORD', answer: 'NOKIA2016\r' }
      ]
    },
    {
      'type': 'telnet',
      'name': 'SHMME04BNK',
      'host': '127.0.0.1',
      'port': '51007',
      'login': [
        { prompt: 'USERNAME', answer: 'NOKIA1\r' },
        { prompt: 'PASSWORD', answer: 'NOKIA2016\r' }
      ]
    },
    {
      'type': 'telnet',
      'name': 'SHMME05BNK',
      'host': '127.0.0.1',
      'port': '51082',
      'login': [
        { prompt: 'USERNAME', answer: 'NOKIA1\r' },
        { prompt: 'PASSWORD', answer: 'NOKIA2016\r' }
      ]
    },
    {
      'type': 'telnet',
      'name': 'SHMME06BNK',
      'host': '127.0.0.1',
      'port': '51001',
      'login': [
        { prompt: 'USERNAME', answer: 'NOKIA1\r' },
        { prompt: 'PASSWORD', answer: 'NOKIA2016\r' }
      ]
    },
    {
      'type': 'telnet',
      'name': 'SHMME07BNK',
      'host': '172.20.2.252',
      'port': '51003',
      'login': [
        { prompt: 'USERNAME', answer: 'NOKIA1\r' },
        { prompt: 'PASSWORD', answer: 'NOKIA2016\r' }
      ]
    },
    {
      'type': 'telnet',
      'name': 'SHMME08BNK',
      'host': '127.0.0.1',
      'port': '51005',
      'login': [
        { prompt: 'USERNAME', answer: 'NOKIA1\r' },
        { prompt: 'PASSWORD', answer: 'NOKIA2016\r' }
      ]
    },
    {
      'type': 'telnet',
      'name': 'SHMME09BNK',
      'host': '127.0.0.1',
      'port': '51028',
      'login': [
        { prompt: 'USERNAME', answer: 'NOKIA1\r' },
        { prompt: 'PASSWORD', answer: 'NOKIA2016\r' }
      ]
    },
    {
      'type': 'telnet',
      'name': 'SHMME10BNK',
      'host': '127.0.0.1',
      'port': '51029',
      'login': [
        { prompt: 'USERNAME', answer: 'NOKIA1\r' },
        { prompt: 'PASSWORD', answer: 'NOKIA2016\r' }
      ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW03BNK',
        'host' : '127.0.0.1',
        'port' : '51008',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW04BNK',
        'host' : '127.0.0.1',
        'port' : '51016',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW05BNK',
        'host' : '127.0.0.1',
        'port' : '51011',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW06BNK',
        'host' : '127.0.0.1',
        'port' : '51012',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW07BNK',
        'host' : '127.0.0.1',
        'port' : '51009',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW08BNK',
        'host' : '127.0.0.1',
        'port' : '51010',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW09BNK',
        'host' : '127.0.0.1',
        'port' : '51006',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW10BNK',
        'host' : '127.0.0.1',
        'port' : '51031',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW11BNK',
        'host' : '127.0.0.1',
        'port' : '51032',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW12BNK',
        'host' : '127.0.0.1',
        'port' : '51033',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
            'type' : 'ssh',
            'name' : 'SHCG16BNK-1',
            'host' : '127.0.0.1',
            'port' : '51052',
            'user' : 'cmd',
            'login': [
            { prompt: 'password:', answer: 'cgadmin!\n' }
            ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG16BNK-2',
        'host' : '127.0.0.1',
        'port' : '51053',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG17BNK-1',
        'host' : '127.0.0.1',
        'port' : '51087',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG17BNK-2',
        'host' : '127.0.0.1',
        'port' : '51088',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG18BNK-1',
        'host' : '127.0.0.1',
        'port' : '51089',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG18BNK-2',
        'host' : '127.0.0.1',
        'port' : '51092',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG19BNK-1',
        'host' : '127.0.0.1',
        'port' : '51126',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG19BNK-2',
        'host' : '127.0.0.1',
        'port' : '51127',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG20BNK-1',
        'host' : '127.0.0.1',
        'port' : '51086',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG20BNK-2',
        'host' : '127.0.0.1',
        'port' : '51085',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG21BNK-1',
        'host' : '127.0.0.1',
        'port' : '51093',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG21BNK-2',
        'host' : '127.0.0.1',
        'port' : '51094',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG22BNK-1',
        'host' : '127.0.0.1',
        'port' : '51095',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG22BNK-2',
        'host' : '127.0.0.1',
        'port' : '51096',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG23BNK-1',
        'host' : '127.0.0.1',
        'port' : '51097',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG23BNK-2',
        'host' : '127.0.0.1',
        'port' : '51098',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG24BNK-1',
        'host' : '127.0.0.1',
        'port' : '51099',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG24BNK-2',
        'host' : '127.0.0.1',
        'port' : '51101',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG25BNK-1',
        'host' : '127.0.0.1',
        'port' : '51102',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG25BNK-2',
        'host' : '127.0.0.1',
        'port' : '51103',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG26BNK-1',
        'host' : '127.0.0.1',
        'port' : '51104',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG26BNK-2',
        'host' : '127.0.0.1',
        'port' : '51105',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG27BNK-1',
        'host' : '127.0.0.1',
        'port' : '51106',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG27BNK-2',
        'host' : '127.0.0.1',
        'port' : '51107',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG28BNK-1',
        'host' : '127.0.0.1',
        'port' : '51108',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG28BNK-2',
        'host' : '127.0.0.1',
        'port' : '51109',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG29BNK-1',
        'host' : '127.0.0.1',
        'port' : '51118',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG29BNK-2',
        'host' : '127.0.0.1',
        'port' : '51119',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG30BNK-1',
        'host' : '127.0.0.1',
        'port' : '51124',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG30BNK-2',
        'host' : '127.0.0.1',
        'port' : '51125',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    }
];

module.exports = netelements; 