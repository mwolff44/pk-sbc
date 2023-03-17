package models

import (
	"fmt"
	"time"
)

// Gateway is the main gateway model
type Gateway struct {
	ID        uint      `json:"id" gorm:"primarykey"`                                                     // Gateway ID
	CreatedAt time.Time `json:"created_at"`                                                               // Creation time
	UpdatedAt time.Time `json:"updated_at"`                                                               // Updated time
	Name      string    `json:"name" binding:"required" gorm:"not null:true"`                             // Name of the gateway
	IpAddress string    `json:"ipaddress" binding:"required,ip" gorm:"not null:true"`                     // IP Address of the gateway
	Port      string    `json:"port"  binding:"required,numeric,max=5" gorm:"not null:true,default:5060"` // SIP Port of the gateway
	Protocol  string    `json:"protocol"  binding:"required,oneof=udp tcp tls" gorm:"default:udp"`        // Protocol used by the gateway
}

// Getaways represents many gateways
type Gateways []Gateway

// GetGateway queries the DB to find a user by ID
func GetGateway(gateway *Gateway, id string) error {
	if err := DB.First(gateway, id).Error; err != nil {
		return err
	}
	return nil
}

// GetGateways queries the DB to find gateways with offset and limit
func GetGateways(gateways *Gateways, gatewaysPerPage int, offset int) error {
	if err := DB.Limit(gatewaysPerPage).Offset(offset).Find(gateways).Error; err != nil {
		return err
	}
	return nil
}

// CountGateways counts gateways in DB
func CountGateways() (int64, error) {
	var gatewayCount int64
	if err := DB.Table("gateways").Count(&gatewayCount).Error; err != nil {
		return 0, err
	}
	return gatewayCount, nil
}

// CreateGateway creates a new gateway
func CreateGateway(gateway *Gateway) error {
	req := DB.Create(gateway)
	if req.RowsAffected == 0 {
		return fmt.Errorf(fmt.Sprintf("gateway not saved: %v", req.Error))
	}
	return nil
}

// UpdateGateway updates a gateway
func UpdateGateway(gateway *Gateway) error {
	if err := DB.Save(&gateway).Error; err != nil {
		return err
	}
	return nil
}

// DeleteGateway deletes a gateway
func DeleteGateway(id string) error {
	if err := DB.Delete(&Gateway{}, id).Error; err != nil {
		return err
	}
	return nil
}

// FindGatewayByName finds gateway by Iname
func FindGatewayByName(name string) (*Gateway, error) {
	gateway := &Gateway{}
	err := DB.Where("uname=?", name).Find(&gateway).Error
	if err != nil {
		return nil, err
	}
	return gateway, nil
}

// FindGatewayByIP finds gateway by IP address
func FindGatewayByIP(ip uint) (*Gateway, error) {
	gateway := &Gateway{}
	err := DB.Where("IpAddress=?", ip).Find(&gateway).Error
	if err != nil {
		return nil, err
	}
	return gateway, nil
}
