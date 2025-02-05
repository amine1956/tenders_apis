def add_info(info_list,tender):
    '''type'''
    type = info_list[1]
    tender.append(type)
    '''Package number'''
    package_number = info_list[2]
    tender.append(package_number)
    '''Post Date'''
    Post_Date = info_list[3]
    tender.append(Post_Date)
    '''Closing Date'''
    Closing_Date = info_list[4]
    tender.append(Closing_Date)
    '''Currency'''
    Currency = info_list[5]
    tender.append(Currency)
    '''Price'''
    Price = info_list[6]
    tender.append(Price)
    '''Description'''
    Description = info_list[7]
    tender.append(Description)
    '''Additional Information'''
    Additional_Info = info_list[8]
    tender.append(Additional_Info)
    '''Source of Funds'''
    sof = info_list[9]
    tender.append(sof)
    '''number of Lots'''
    Lots = info_list[10]
    tender.append(Lots)
    '''Agency'''
    Agency = info_list[11]
    tender.append(Agency)
    '''Region'''
    Region = info_list[12]
    tender.append(Region)
    '''District'''
    District = info_list[13]
    tender.append(District)
    '''Contact Person'''
    Contact = info_list[14]
    tender.append(Contact)
    '''Email'''
    Email = info_list[15]
    tender.append(Email)
    '''Telphone'''
    Telphone = info_list[16]
    tender.append(Telphone)
    '''Fax'''
    Fax = info_list[17]
    tender.append(Fax)
    '''Website'''
    Website = info_list[18]
    tender.append(Website)
    
    return tender