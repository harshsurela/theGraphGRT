from .models import transactions

def addTransaction(amount,userId,credited,tag,status):
    transObj = transactions()
    transObj.amount = amount
    transObj.user_id = userId
    transObj.credited = credited
    transObj.tag = tag
    transObj.payment_status = status
    transObj.save()
    
def findReferrals(user, level=0,tmp=None):
    # referrals_list = []
    if tmp is None:
        tmp = {}
        
    
    referrals = user.ref_user.all()
    if len(referrals) > 0:
        tmp[user.mobile_number] = [referrals,level]
    for referral in referrals:
        # referrals_list.append((referral, level))
        findReferrals(referral, level + 1,tmp)
    
    return tmp
    