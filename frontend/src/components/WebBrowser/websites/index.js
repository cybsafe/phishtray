import MyPayment from './MyPayment';
import Bluestar from './Bluestar';
import Blocked from './Blocked';
import Warning from './Warning';

export default {
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
  bluestarFalse: {
    isSecure: true,
    url: 'www.bluestarr.com',
    component: Bluestar,
    link: 'bluestarfalse',
  },
  bluestarFalseInsecure: {
    isSecure: false,
    url: 'www.bluestarr.com',
    component: Bluestar,
    link: 'bluestarFalseInsecure',
  },
  blockedPage: {
    isSecure: true,
    url: 'www.myblockedpage.info',
    component: Blocked,
    link: 'myblocked',
  },
  warning: {
    isSecure: true,
    url: 'www.warningpage.com',
    component: Warning,
    link: 'warninglink',
  },
};
