def polymorphic_subclasses(class_):
    return {discriminator: mapper.class_ for discriminator, mapper in class_.__mapper__.polymorphic_map.items()}

def polymorphic_subclass(class_, discriminator):
    return class_.__mapper__.polymorphic_map[discriminator].class_
