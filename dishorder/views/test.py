@dishorderapi.route('/edit-supplier', methods=['PUT'])
def edit_supplier():
    if request.is_json:
        current_code = request.json.get('current_code')
        code_change_to = request.json.get('code_change_to', '')
        is_code_existed = session.query(Suppliers).filter(Suppliers.code == code_change_to).first()
        if current_code != code_change_to:
            if is_code_existed:
                msg = ReturnMSG().fail_cheat
                msg['msg'] = 'Supplier code {} existed'.format(code_change_to)
                return jsonify(msg)
            else:
                pass
        else:
            pass
        name = request.json.get('name', '')
        email_address = request.json.get('email_address', '')
        supplier_current_email = session.query(Suppliers).filter_by(code=code_change_to).first()
        if supplier_current_email.email_address != email_address:
            check_email = session.query(Suppliers).filter_by(email_address=email_address).first()
            if check_email:
                msg = ReturnMSG().fail_cheat
                msg['msg'] = 'Supplier email {} existed'.format(email_address)
                return jsonify(msg)
        phone = request.json.get('phone', '')
        contact_name = request.json.get('contact_name', '')
        currency = request.json.get('currency', '')
        uploaded_img_name = request.json.get('uploaded_img_name')
        supplier_need_to_edit = session.query(Suppliers).filter_by(code=current_code).first()
        if uploaded_img_name:
            new_supplier_photo = Photos(photo_type='supplier',
                                        type_id=0,
                                        path=uploaded_img_name)
            session.add(new_supplier_photo)
            session.commit()
            uploaded_img_id = session.query(Photos).filter_by(path=uploaded_img_name).first().id
            photo_default_id = uploaded_img_id
        else:
            photo_default_id = supplier_need_to_edit.photo_default_id
        order_time_deadline = hour_minute_to_timestamp(request.json.get('order_time_deadline', 0))
        minimum_order_quantity = int(request.json.get('min_quantity', '-1'))
        minimum_order_amount = int(request.json.get('min_amount', '-1'))
        if False:
            return jsonify(ReturnMSG().wrong_post_format)
        else:
            new_supplier_check_obj = Suppliers(code=code_change_to, name=name, email_address=email_address, phone=phone,
                                               contact_name=contact_name, photo_thumbnail=b'', currency=currency,
                                               photo_default_id=photo_default_id,
                                               order_time_deadline=order_time_deadline,
                                               minimum_order_quantity=minimum_order_quantity,
                                               minimum_order_amount=minimum_order_amount,
                                               review=0, popularity=0)
            validation_return = new_supplier_check_obj.validation
            if not validation_return == "True":
                msg = ReturnMSG().fail_cheat
                msg['msg'] = validation_return
                return jsonify(msg)
            else:
                supplier_need_to_edit.code = code_change_to
                supplier_need_to_edit.name = name
                supplier_need_to_edit.email_address = email_address
                supplier_need_to_edit.phone = phone
                supplier_need_to_edit.contact_name = contact_name
                supplier_need_to_edit.currency = currency
                supplier_need_to_edit.order_time_deadline = order_time_deadline
                supplier_need_to_edit.minimum_order_quantity = int(minimum_order_quantity)
                supplier_need_to_edit.minimum_order_amount = int(minimum_order_amount)
                if photo_default_id:
                    supplier_need_to_edit.photo_default_id = photo_default_id
                else:
                    pass
                session.commit()
                return jsonify(ReturnMSG().register_success)
    else:
        return jsonify(ReturnMSG().wrong_post_format)