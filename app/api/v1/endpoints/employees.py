from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, func, and_, or_
from datetime import datetime, date
import uuid

from app.core.database import get_db
from app.core.security import get_current_active_user, get_password_hash
from app.crud.base import CRUDBase
from app.crud.user import user as crud_user
from app.models.employee import Employee, EmployeeStatus
from app.models.user import User as UserModel
from app.schemas.employee import Employee as EmployeeSchema, EmployeeCreate, EmployeeUpdate
from app.schemas.user import User, UserCreate
from app.schemas.base import PaginatedResponse
from app.api.v1.dependencies import get_pagination_params

# Create CRUD instance
crud_employee = CRUDBase(Employee)

router = APIRouter()

@router.get("/", response_model=PaginatedResponse[EmployeeSchema])
async def read_employees(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(get_pagination_params),
    search: Optional[str] = Query(None, description="Search by name, phone, or email"),
    status: Optional[str] = Query(None, description="Filter by status"),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Retrieve employees from current organization with pagination
    """
    # Base query (sin user_id por ahora)
    query = select(Employee).where(
        and_(
            Employee.organization_id == current_user.organization_id,
            Employee.is_active == True
        )
    )
    
    # Add search filter if provided
    if search:
        search_filter = or_(
            Employee.full_name.ilike(f"%{search}%"),
            Employee.phone.ilike(f"%{search}%"),
            Employee.email.ilike(f"%{search}%") if search else False,
            Employee.document_number.ilike(f"%{search}%")
        )
        query = query.where(search_filter)
    
    # Add status filter if provided
    if status and status in ["active", "inactive"]:
        query = query.where(Employee.status == EmployeeStatus(status))
    
    # Count total
    count_query = select(func.count(Employee.id)).where(
        and_(
            Employee.organization_id == current_user.organization_id,
            Employee.is_active == True
        )
    )
    
    # Add filters to count query
    if search:
        search_filter = or_(
            Employee.full_name.ilike(f"%{search}%"),
            Employee.phone.ilike(f"%{search}%"),
            Employee.email.ilike(f"%{search}%") if search else False,
            Employee.document_number.ilike(f"%{search}%")
        )
        count_query = count_query.where(search_filter)
    
    if status and status in ["active", "inactive"]:
        count_query = count_query.where(Employee.status == EmployeeStatus(status))
    
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Apply pagination
    query = query.offset(pagination["skip"]).limit(pagination["limit"])
    
    # Execute query
    result = await db.execute(query)
    employees = result.scalars().all()
    
    # Calculate pagination info
    pages = (total + pagination["limit"] - 1) // pagination["limit"]
    page = (pagination["skip"] // pagination["limit"]) + 1
    
    return PaginatedResponse(
        items=employees,
        total=total,
        page=page,
        size=pagination["limit"],
        pages=pages
    )

@router.post("/", response_model=EmployeeSchema)
async def create_employee(
    *,
    db: AsyncSession = Depends(get_db),
    employee_in: EmployeeCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create new employee and optionally create user account
    """
    # Check if employee with same document already exists
    existing_query = select(Employee).where(
        and_(
            Employee.document_number == employee_in.document_number,
            Employee.organization_id == current_user.organization_id
        )
    )
    existing_result = await db.execute(existing_query)
    existing_employee = existing_result.scalar_one_or_none()
    
    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Employee with this document number already exists"
        )
    
    # Create user if email and password provided (opcional por ahora)
    user_id = None
    if employee_in.email and employee_in.password:
        try:
            # Check if user with email already exists
            existing_user = await crud_user.get_by_email(db, email=employee_in.email)
            if existing_user:
                raise HTTPException(
                    status_code=400,
                    detail="User with this email already exists"
                )
            
            # Create user
            user_data = UserCreate(
                email=employee_in.email,
                password=employee_in.password,
                role=employee_in.role or "employee",
                organization_id=current_user.organization_id
            )
            user = await crud_user.create(db, obj_in=user_data)
            user_id = user.id
        except Exception as e:
            print(f"Error creating user: {e}")
            # Continuar sin crear usuario si hay error
            pass
    
    # Create employee (let the model handle start_date default)
    employee_data = {
        "full_name": employee_in.full_name,
        "document_type": employee_in.document_type,
        "document_number": employee_in.document_number,
        "email": employee_in.email,
        "phone": employee_in.phone,
        "address": employee_in.address,
        "position": employee_in.position,
        "organization_id": current_user.organization_id,
        "branch_id": employee_in.branch_id,
        "user_id": user_id
    }
    
    # Only add start_date if provided
    if employee_in.start_date:
        if isinstance(employee_in.start_date, str):
            try:
                employee_data["start_date"] = datetime.strptime(employee_in.start_date, '%Y-%m-%d').date()
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="start_date must be in YYYY-MM-DD format"
                )
        else:
            employee_data["start_date"] = employee_in.start_date
    
    employee = await crud_employee.create(db, obj_in=employee_data)
    return employee

@router.get("/{employee_id}", response_model=EmployeeSchema)
async def read_employee(
    *,
    db: AsyncSession = Depends(get_db),
    employee_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get employee by ID
    """
    employee = await crud_employee.get(db, id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Check if employee belongs to current organization
    if employee.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return employee

@router.put("/{employee_id}", response_model=EmployeeSchema)
async def update_employee(
    *,
    db: AsyncSession = Depends(get_db),
    employee_id: uuid.UUID,
    employee_in: EmployeeUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update employee
    """
    employee = await crud_employee.get(db, id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Check if employee belongs to current organization
    if employee.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    employee = await crud_employee.update(db, db_obj=employee, obj_in=employee_in)
    return employee

@router.delete("/{employee_id}", response_model=EmployeeSchema)
async def delete_employee(
    *,
    db: AsyncSession = Depends(get_db),
    employee_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete employee (soft delete)
    """
    employee = await crud_employee.get(db, id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Check if employee belongs to current organization
    if employee.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    employee = await crud_employee.remove(db, id=employee_id)
    return employee

@router.patch("/{employee_id}/toggle-status", response_model=EmployeeSchema)
async def toggle_employee_status(
    *,
    db: AsyncSession = Depends(get_db),
    employee_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Toggle employee status (active/inactive)
    """
    employee = await crud_employee.get(db, id=employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Check if employee belongs to current organization
    if employee.organization_id != current_user.organization_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    # Toggle status
    new_status = EmployeeStatus.INACTIVE if employee.status == EmployeeStatus.ACTIVE else EmployeeStatus.ACTIVE
    
    employee = await crud_employee.update(
        db, 
        db_obj=employee, 
        obj_in={"status": new_status}
    )
    return employee 