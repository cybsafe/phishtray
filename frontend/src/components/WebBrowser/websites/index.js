import MyOffice from './MyOffice';
import MyPayment from './MyPayment';

export default {
  myoffice: {
    isSecure: true,
    url: 'www.myoffice.com',
    component: MyOffice,
  },
  mypayment: {
    isSecure: true,
    url: 'www.moneytransfer.com',
    component: MyPayment,
  },
  mypaymentFalse: {
    isSecure: false,
    url: 'www.moneytransfr.com',
    component: MyPayment,
  },
  mypaymentFalseInsecure: {
    isSecure: true,
    url: 'www.moneytransfr.com',
    component: MyPayment,
  },
};
