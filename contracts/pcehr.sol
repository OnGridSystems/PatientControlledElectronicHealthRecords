pragma solidity ^0.4.0;


contract PCEHR {

    struct Patient {
        bytes32 proxyId;
        bytes32 pubKey;
    }

    struct RecordsSet {
        bool exists;
        bytes32 proxyId;
    }

    struct RecordsRecepient {
        bytes32 realWorldId;
        bytes32 proxyId;
        bytes32 pubKey;
    }

    struct RecepientRights {
        bool canRead;
        bool canExtend;
    }

    mapping (address => Patient) public patients;
    mapping (address => RecordsRecepient) public recepients;
    mapping (address => mapping (bytes32 => RecordsSet)) recordsSets;
    mapping (address => mapping (address => mapping (bytes32 => RecepientRights))) recepientsRights;
    mapping (bytes32 => bool) recordsSetsTypes;

    modifier onlyRegisteredPatient() {
        require(
            patients[msg.sender].proxyId != bytes32(0x0), 
            "Sender is not registered as patient"
        );
        _;
    }

    modifier onlyNotRegisteredPatient() {
        require(
            patients[msg.sender].proxyId == bytes32(0x0), 
            "Sender already registered as patient"
        );
        _;
    }

    modifier onlyRegisteredRecepient() {
        require(
            recepients[msg.sender].proxyId != bytes32(0x0), 
            "Sender is not registered as recepient"
        );
        _;
    }

    modifier onlyNotRegisteredRecepient() {
        require(
            recepients[msg.sender].proxyId == bytes32(0x0), 
            "Sender already registered as recepient"
        );
        _;
    }

    modifier onlyHasReadRightsRecepient(
        address _patientAddress,
        bytes32 _recordsType
    ) {
        require(
            recepientsRights[_patientAddress][msg.sender][_recordsType].canRead,
            "Sender has no read rights for this records set"
        );
        _;
    }

    modifier onlyHasExtendRightsRecepient(
        address _patientAddress,
        bytes32 _recordsType
    ) {
        require(
            recepientsRights[_patientAddress][msg.sender][_recordsType].canExtend,
            "Sender has no extend rights for this records set"
        );
        _;
    }

    modifier onlyPatientHasRecordsSetType(bytes32 _recordsType) {
        require(
            recordsSets[msg.sender][_recordsType].exists,
            "Sender has no records set of this type"
        );
        _;
    }

    modifier onlyNonExistedRecordsSet(bytes32 _recordsType) {
        require(
            !recordsSets[msg.sender][_recordsType].exists,
            "Records set with this proxyId already exists"
        );
        _;
    }

    modifier validRecordsSetType(bytes32 _recordsType) {
        require(
            recordsSetsTypes[_recordsType],
            "Invalid records set type"
        );
        _;
    }

    event PatientInChain(
        address _address,
        bytes32 _pubKey,
        bytes32 indexed _patientProxyId
    );

    event RecepientInChain(
        address _address,
        bytes32 _pubKey,
        bytes32 indexed _recepientProxyId,
        bytes32 indexed _realWorldId
    );

    event RecordsSetAdded(
        address _addedBy,
        bytes32 _recordsSetProxyId,
        bytes32 _recordsType
    );

    event RecordsSetExtended(
        address _extendedBy,
        bytes32 _recordsSetProxyId
    );

    event AllowedExtendAccessToRecordsSet(
        bytes32 _recordsSetProxyId,
        address indexed _recepientAddress
    );

    event AllowedReadAccessToRecordsSet(
        bytes32 _recordsSetProxyId,
        address indexed _toRecepientAddress
    );

    constructor(bytes32[] _recordsSetsTypes) public {
        for (uint i = 0; i < _recordsSetsTypes.length; i++) {
            recordsSetsTypes[_recordsSetsTypes[i]] = true;
        }
    }

    function registerPatient(
        bytes32 _patientProxyId,
        bytes32 _patientPubKey
    )
    public
    onlyNotRegisteredRecepient()
    onlyNotRegisteredPatient()
    {
        var patient = Patient(_patientProxyId, _patientPubKey);
        patients[msg.sender] = patient;

        emit PatientInChain(
            msg.sender,
            _patientPubKey,
            _patientProxyId
        );

    }

    function registerRecepient(
        bytes32 _recepientProxyId,
        bytes32 _recepientPubKey,
        bytes32 _recepientRealWorldId
    )
    public
    onlyNotRegisteredPatient()
    onlyNotRegisteredRecepient()
    {
        var recepient = RecordsRecepient(
            _recepientProxyId,
            _recepientPubKey,
            _recepientRealWorldId
        );
        recepients[msg.sender] = recepient;

        emit RecepientInChain(
            msg.sender,
            _recepientPubKey,
            _recepientProxyId,
            _recepientRealWorldId
        );
    }

    function addRecordsSet(
        address _patientAddress,
        bytes32 _proxyId,
        bytes32 _recordsType
    ) 
    public
    validRecordsSetType(_recordsType)
    onlyNonExistedRecordsSet(_recordsType)
    onlyHasExtendRightsRecepient(_patientAddress, _recordsType)
    {
        recordsSets[_patientAddress][_recordsType] = RecordsSet(true, _proxyId);

        emit RecordsSetAdded(msg.sender, _proxyId, _recordsType);       
    }

    function extendRecordsSet(
        address _patientAddress,
        bytes32 _recordsType
    )
    public
    validRecordsSetType(_recordsType)
    onlyHasExtendRightsRecepient(_patientAddress, _recordsType)
    {
        emit RecordsSetExtended(
            msg.sender,
            recordsSets[_patientAddress][_recordsType].proxyId
        );
    }

    function allowRecordsSetReadRights(
        bytes32 _recordsSetType,
        address _toRecepientAddress
    )
    public
    onlyRegisteredPatient()
    validRecordsSetType(_recordsSetType)
    onlyPatientHasRecordsSetType(_recordsSetType)
    {
        recepientsRights[msg.sender][_toRecepientAddress][_recordsSetType] = RecepientRights(true, false);
        bytes32 proxyId = recordsSets[msg.sender][_recordsSetType].proxyId;

        emit AllowedReadAccessToRecordsSet(proxyId, _toRecepientAddress);
    }

    function allowRecordsSetExtendRights(
        bytes32 _recordsSetType,
        address _toRecepientAddress
    )
    public
    onlyRegisteredPatient()
    validRecordsSetType(_recordsSetType)
    onlyPatientHasRecordsSetType(_recordsSetType)
    {
        recepientsRights[msg.sender][_toRecepientAddress][_recordsSetType] = RecepientRights(true, true);
        bytes32 proxyId = recordsSets[msg.sender][_recordsSetType].proxyId;

        emit AllowedExtendAccessToRecordsSet(proxyId, _toRecepientAddress);
    }
}
