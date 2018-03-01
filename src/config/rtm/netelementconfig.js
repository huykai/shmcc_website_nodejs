'use strict';
var netelements = [ 
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
        'type': 'telnet',
        'name': 'SHMME05BNK',
        'host': '172.20.12.60',
        'port': '23',
        'login': [
        { prompt: 'USERNAME', answer: 'NOKIA1\r' },
        { prompt: 'PASSWORD', answer: 'NOKIA2016\r' }
        ]
    },
    {
        'type': 'telnet',
        'name': 'SHMME06BNK',
        'host': '172.20.2.220',
        'port': '23',
        'login': [
        { prompt: 'USERNAME', answer: 'NOKIA1\r' },
        { prompt: 'PASSWORD', answer: 'NOKIA2016\r' }
        ]
    },
    {
        'type': 'telnet',
        'name': 'SHMME07BNK',
        'host': '172.20.2.252',
        'port': '23',
        'login': [
        { prompt: 'USERNAME', answer: 'NOKIA1\r' },
        { prompt: 'PASSWORD', answer: 'NOKIA2016\r' }
        ]
    },
    {
        'type': 'telnet',
        'name': 'SHMME08BNK',
        'host': '172.20.13.60',
        'port': '23',
        'login': [
        { prompt: 'USERNAME', answer: 'NOKIA1\r' },
        { prompt: 'PASSWORD', answer: 'NOKIA2016\r' }
        ]
    },
    {
        'type': 'telnet',
        'name': 'SHMME09BNK',
        'host': '172.20.26.116',
        'port': '23',
        'login': [
        { prompt: 'USERNAME', answer: 'NOKIA1\r' },
        { prompt: 'PASSWORD', answer: 'NOKIA2016\r' }
        ]
    },
    {
        'type': 'telnet',
        'name': 'SHMME10BNK',
        'host': '172.20.26.180',
        'port': '23',
        'login': [
        { prompt: 'USERNAME', answer: 'NOKIA1\r' },
        { prompt: 'PASSWORD', answer: 'NOKIA2016\r' }
        ]
    }, 
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW03BNK',
        'host' : '172.20.14.129',
        'port' : '22',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW04BNK',
        'host' : '172.20.15.161',
        'port' : '22',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW05BNK',
        'host' : '172.20.25.128',
        'port' : '22',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW06BNK',
        'host' : '172.20.25.136',
        'port' : '22',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW07BNK',
        'host' : '172.20.25.144',
        'port' : '22',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW08BNK',
        'host' : '172.20.2.81',
        'port' : '22',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW09BNK',
        'host' : '172.20.2.97',
        'port' : '22',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW10BNK',
        'host' : '172.20.24.161',
        'port' : '22',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW11BNK',
        'host' : '172.20.24.209',
        'port' : '22',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHSAEGW12BNK',
        'host' : '172.20.26.161',
        'port' : '22',
        'user' : 'nokia1',
        'login': [
        { prompt: 'password:', answer: 'qz76gprs\n' }
        ]
    },
    {
            'type' : 'ssh',
            'name' : 'SHCG16BNK-1',
            'host' : '172.20.25.88',
            'port' : '22',
            'user' : 'cmd',
            'login': [
            { prompt: 'password:', answer: 'cgadmin!\n' }
            ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG16BNK-2',
        'host' : '172.20.25.89',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG17BNK-1',
        'host' : '172.20.14.167',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG17BNK-2',
        'host' : '172.20.14.168',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG18BNK-1',
        'host' : '172.20.14.176',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG18BNK-2',
        'host' : '172.20.14.177',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG19BNK-1',
        'host' : '172.20.25.70',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG19BNK-2',
        'host' : '172.20.25.71',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG20BNK-1',
        'host' : '172.20.25.79',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG20BNK-2',
        'host' : '172.20.25.80',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG21BNK-1',
        'host' : '172.20.25.199',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG21BNK-2',
        'host' : '172.20.25.200',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG22BNK-1',
        'host' : '172.20.25.208',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG22BNK-2',
        'host' : '172.20.25.209',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG23BNK-1',
        'host' : '172.20.25.217',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG23BNK-2',
        'host' : '172.20.25.218',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG24BNK-1',
        'host' : '172.20.25.226',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG24BNK-2',
        'host' : '172.20.25.227',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG25BNK-1',
        'host' : '172.20.24.231',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG25BNK-2',
        'host' : '172.20.24.232',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG26BNK-1',
        'host' : '172.20.24.240',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG26BNK-2',
        'host' : '172.20.24.241',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG27BNK-1',
        'host' : '172.20.30.9',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG27BNK-2',
        'host' : '172.20.30.10',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG28BNK-1',
        'host' : '172.20.30.18',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG28BNK-2',
        'host' : '172.20.30.19',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG29BNK-1',
        'host' : '172.20.30.27',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG29BNK-2',
        'host' : '172.20.30.28',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG30BNK-1',
        'host' : '172.20.30.36',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    },
    {
        'type' : 'ssh',
        'name' : 'SHCG30BNK-2',
        'host' : '172.20.30.37',
        'port' : '22',
        'user' : 'cmd',
        'login': [
        { prompt: 'password:', answer: 'cgadmin!\n' }
        ]
    }
];

module.exports = netelements; 