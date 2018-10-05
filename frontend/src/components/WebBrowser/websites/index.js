import MyOffice from './MyOffice';
import MyPayment from './MyPayment';
import Bluestar from './Bluestar';

export default {
  myoffice: {
    isSecure: true,
    url: 'www.myoffice.com',
    component: MyOffice,
    link: 'myoffice',
  },
  mypayment: {
    isSecure: true,
    url: 'www.moneytransfer.com',
    component: MyPayment,
    link: 'mypayment',
  },
  mypaymentFalse: {
    isSecure: false,
    url: 'www.moneytransfr.com',
    component: MyPayment,
    link: 'mypaymentFalse',
  },
  mypaymentFalseInsecure: {
    isSecure: true,
    url: 'www.moneytransfr.com',
    component: MyPayment,
    link: 'mypaymentFalseInsecure',
  },
  bluestar: {
    isSecure: true,
    url: 'www.bluestar.com',
    component: Bluestar,
    link: 'bluestar',
  },
};
