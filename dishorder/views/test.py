if request.is_json:
    code = request.json.get('code', None)
    name = request.json.get('name', None)
    email_address = request.json.get('email_address', None)
    phone = request.json.get('phone', None)
    contact_name = request.json.get('contact_name', None)
    currency = request.json.get('currency', None)
    uploaded_img_name = request.json.get('uploaded_img_name', None)
    order_time_deadline = request.json.get('order_time_deadline', None)
    minimum_order_quantity = request.json.get('min_quantity', None)
    minimum_order_amount = request.json.get('min_amount', None)
    review = 0
    popularity = 0
    if not code or not name or not email_address or not phone or not contact_name \
                or not currency or not order_time_deadline or not minimum_order_quantity \
                or not minimum_order_amount:
        return jsonify(ReturnMSG().wrong_post_format)
    else:
        is_code_existed = session.query(Suppliers).filter(Suppliers.code == code).first()
        if not is_code_existed:
            is_email_existed = session.query(Suppliers).filter(Suppliers.email_address == email_address).first()
            if not is_email_existed:
                if isinstance(safe_cast(minimum_order_quantity, int), int) \
                    and isinstance(safe_cast(minimum_order_amount, int), int):
                    if uploaded_img_name:
                        new_supplier_photo = Photos(photo_type='supplier',
                                                    type_id=0,
                                                    path=uploaded_img_name)
                        session.add(new_supplier_photo)
                        session.commit()
                        uploaded_img_id = session.query(Photos).filter_by(path=uploaded_img_name).first().id
                        photo_default_id = uploaded_img_id
                    else:
                        photo_default_id = 1
                    new_supplier = Suppliers(code=code, name=name, email_address=email_address, phone=phone,
                                             contact_name=contact_name, photo_thumbnail=photo_thumbnail,
                                             currency=currency,
                                             photo_default_id=photo_default_id, order_time_deadline=order_time_deadline,
                                             minimum_order_quantity=minimum_order_quantity,
                                             minimum_order_amount=minimum_order_amount,
                                             review=review, popularity=popularity)
                    session.add(new_supplier)
                    session.commit()
                    return jsonify(ReturnMSG().register_success)
                else:
                    msg = ReturnMSG().fail_cheat
                    msg['msg'] = 'Order quantity or Order amount contain invalid character'
                    return jsonify(msg)
            else:
                msg = ReturnMSG().fail_cheat
                msg['msg'] = 'Supplier email {} existed'.format(email_address)
                return jsonify(msg)
        else:
            msg = ReturnMSG().fail_cheat
            msg['msg'] = 'Supplier code {} existed'.format(code)
            return jsonify(msg)