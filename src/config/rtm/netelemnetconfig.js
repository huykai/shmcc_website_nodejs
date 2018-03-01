mmes = [ 
    {
      'type' : 'telnet',
      'name' : 'SHMME03BNK',
      'host' : '172.20.13.28',
      'port' : '23',
      'login': [
        { prompt: 'USERNAME', answer: 'NOKIA1\r' },
        { prompt: 'PASSWORD', answer: 'NOKIA2016\r' }
      ]
    },
    {
      'type': 'telnet',
      'name': 'SHMME04BNK',
      'host': '172.20.12.28',
      'port': '23',
      'login': [
        { prompt: 'USERNAME', answer: 'NOKIA1\r' },
        { prompt: 'PASSWORD', answer: 'NOKIA2016\r' }
      ]
    },
    {
      'type': 'ssh',
      'name': 'CENTOS7',
      'host': '10.20.0.231',
      'port': '22',
      'user': 'huykai',
      'login': [
        { prompt: 'password:', answer: 'Huykai123\n' }
      ]
    }
];

saegws = [ 
  {
    'type' : 'ssh',
    'name' : 'SHSAEGW03BNK',
    //'address': '172.20.13.28',
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
    //'address': '172.20.12.28',
    'host' : '127.0.0.1',
    'port' : '51016',
    'user' : 'nokia1',
    'login': [
      { prompt: 'password:', answer: 'qz76gprs\n' }
    ]
  }
];

cgs = [ 
  {
    'type' : 'ssh',
    'name' : 'SHCG17BNK-1',
    //'address': '172.20.13.28',
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
    //'address': '172.20.12.28',
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
    //'address': '172.20.13.28',
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
    //'address': '172.20.12.28',
    'host' : '127.0.0.1',
    'port' : '51092',
    'user' : 'cmd',
    'login': [
      { prompt: 'password:', answer: 'cgadmin!\n' }
    ]
  }
];